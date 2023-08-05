# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Proxy for models produced by AutoML."""
import datetime
import logging
import os
import pickle
import shutil
import tempfile
from typing import Any, Optional, Tuple, TYPE_CHECKING, Union


from azureml._base_sdk_common._docstring_wrapper import experimental
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.constants import TelemetryConstants
from azureml.automl.core.shared.exceptions import ClientException, ConfigException, ScenarioNotSupportedException
from azureml.automl.core.shared._diagnostics.automl_error_definitions import \
    DataPathNotFound, \
    InvalidArgumentType, \
    RemoteInferenceUnsupported
from azureml.core import Dataset, Run, RunConfiguration, ScriptRunConfig
from azureml.core.compute import ComputeTarget
from azureml.data.abstract_dataset import AbstractDataset
from azureml.data.dataset_error_handling import DatasetValidationError
from azureml.exceptions import UserErrorException
from .constants import LOCAL_PREDICT_NAME, PREDICT_INPUT_FILE, SCRIPT_RUN_ID_PROPERTY
from ._local_managed_utils import handle_data
if TYPE_CHECKING:
    from pandas import Timestamp
else:
    Timestamp = Any


PREDICT = "predict"
PREDICT_PROBA = "predict_proba"
FORECAST = "forecast"
RESULTS_PROPERTY = "inference_results"

logger = logging.getLogger(__name__)


@experimental
class ModelProxy:
    """Proxy object for AutoML models that enables inference on remote compute."""

    def __init__(self, child_run, compute_target=None):
        """
        Create an AutoML ModelProxy object to submit inference to the training environment.

        :param child_run: The child run from which the model will be downloaded.
        :param compute_target: Overwrite for the target compute to inference on.
        """
        if not isinstance(child_run, Run):
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType, target="child_run",
                    argument="child_run", actual_type=type(child_run), expected_types="azureml.core.Run")
            )
        self.run = child_run
        if compute_target is not None:
            if isinstance(compute_target, ComputeTarget):
                self.compute_target = compute_target.name
            elif isinstance(compute_target, str):
                self.compute_target = compute_target
            else:
                raise ConfigException._with_error(
                    AzureMLError.create(
                        InvalidArgumentType, target="compute_target",
                        argument="compute_target", actual_type=type(compute_target),
                        expected_types="str, azureml.core.compute.ComputeTarget"
                    )
                )
        else:
            self.compute_target = child_run._run_dto.get('target')

    def _fetch_env(self):
        script_run_id = self.run.parent.get_properties().get(SCRIPT_RUN_ID_PROPERTY)
        if script_run_id is None:
            try:
                env = self.run.get_environment()
            except Exception as e:
                if isinstance(e, KeyError) or \
                        "There is no run definition or environment specified for the run." in str(e) or \
                        "There is no environment specified for the run" in str(e):
                    raise ScenarioNotSupportedException._with_error(
                        AzureMLError.create(
                            RemoteInferenceUnsupported, target="model_proxy"
                        )
                    )
                raise
        else:
            script_run = Run(self.run.experiment, script_run_id)
            env = script_run.get_environment()
        return env

    def _fetch_results(self, inference_results_path: str, script_run: Run) \
            -> Union[AbstractDataset, Tuple[AbstractDataset, AbstractDataset]]:
        datastore = self.run.experiment.workspace.get_default_datastore()
        results_locations = script_run.get_properties().get(RESULTS_PROPERTY)
        if results_locations is None:
            # <=1.10 does not format the inference_results_path
            # Remove once curated env for 1.11 rolls out. Model proxy only started being supported for 1.11, so
            # we can deprecate after just 1 release.
            returned_values = Dataset.Tabular.from_delimited_files(path=[(datastore, inference_results_path)])  \
                # type: Union[AbstractDataset, Tuple[AbstractDataset, AbstractDataset]]
        else:
            results_locations = eval(results_locations)
            if len(results_locations) == 1:
                returned_values = Dataset.Tabular.from_delimited_files(path=[(datastore, results_locations[0])])
            else:
                # some inference methods can return tuples, format appropriately
                returned_values = ()
                for location in results_locations:
                    returned_values += (Dataset.Tabular.from_delimited_files(path=[(datastore, location)]),)

        return returned_values

    def _inference(self, function_name: str, values: Any, y_values: Optional[Any] = None) \
            -> Union[AbstractDataset, Tuple[AbstractDataset, AbstractDataset]]:
        logger.info("Submitting inference job.")

        with logging_utilities.log_activity(logger, activity_name=TelemetryConstants.REMOTE_INFERENCE):
            with tempfile.TemporaryDirectory() as project_folder:
                with open(os.path.join(project_folder, PREDICT_INPUT_FILE), "wb+") as file:
                    pickle.dump((values, y_values), file)
                    data_dict = {"values": values, "y_values": y_values}
                    data_args = handle_data(data_dict, project_folder)

                run_configuration = RunConfiguration()

                env = self._fetch_env()

                run_configuration.environment = env
                run_configuration.target = self.run._run_dto.get('target', 'local')

                # TODO, how to enable docker for local inference?
                # run_configuration.environment.docker.enabled = docker

                if self.compute_target is not None:
                    run_configuration.target = self.compute_target

                package_dir = os.path.dirname(os.path.abspath(__file__))
                script_path = os.path.join(package_dir, LOCAL_PREDICT_NAME)
                shutil.copy(script_path, os.path.join(project_folder, LOCAL_PREDICT_NAME))

                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                inference_results_path = "{}_{}_{{}}".format(self.run.id, timestamp)

                data_args.extend(["--child_run_id", self.run.id,
                                  "--function_name", function_name,
                                  "--inference_results_path", inference_results_path])

                src = ScriptRunConfig(source_directory=project_folder,
                                      script=LOCAL_PREDICT_NAME,
                                      run_config=run_configuration,
                                      arguments=data_args)

                logger.info("Submitting script run for inferencing.")
                script_run = self.run.submit_child(src)

                logger.info("Waiting for script run for inferencing to complete.")
                script_run.wait_for_completion(show_output=False, wait_post_processing=True)

                logger.info("Inferencing complete.")
                return self._fetch_results(inference_results_path, script_run)

    @experimental
    def predict(self, values: Any) -> AbstractDataset:
        """
        Submit a job to run predict on the model for the given values.

        :param values: Input test data to run predict on.
        :type values: AbstractDataset or pandas.DataFrame or numpy.ndarray
        :return: The predicted values.
        """
        return self._inference(PREDICT, values)

    @experimental
    def predict_proba(self, values: Any) -> AbstractDataset:
        """
        Submit a job to run predict_proba on the model for the given values.

        :param values: Input test data to run predict on.
        :type values: AbstractDataset or pandas.DataFrame or numpy.ndarray
        :return: The predicted values.
        """
        return self._inference(PREDICT_PROBA, values)

    @experimental
    def forecast(self, X_values: Any, y_values: Optional[Any] = None) -> Tuple[AbstractDataset, AbstractDataset]:
        """
        Submit a job to run forecast on the model for the given values.

        :param X_values: Input test data to run forecast on.
        :type X_values: AbstractDataset or pandas.DataFrame or numpy.ndarray
        :param y_values: Input y values to run the forecast on.
        :type y_values: AbstractDataset or pandas.DataFrame or numpy.ndarray
        :return: The forecast values.
        """
        return self._inference(FORECAST, X_values, y_values)
