# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import argparse
import logging
import os
import pickle as pkl
from typing import Any, Optional, TYPE_CHECKING

from azureml._history.utils.constants import LOGS_AZUREML_DIR
from azureml.automl.core.shared import log_server
from azureml.core import Run, Dataset, Workspace
from azureml.data.abstract_dataset import AbstractDataset
import azureml.train.automl
from azureml.train.automl import _logging
from azureml.train.automl.constants import AUTOML_SETTINGS_PATH, AUTOML_FIT_PARAMS_PATH, MANAGED_RUN_ID_PARAM
from azureml.train.automl._azureautomlclient import AzureAutoMLClient
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
try:
    from azureml.automl.core.shared.pickler import DefaultPickler
except ImportError:
    if not TYPE_CHECKING:
        from azureml.automl.runtime.shared.pickler import DefaultPickler
try:
    from azureml.train.automl._local_managed_utils import get_data
except ImportError:
    def _get_dataset(workspace: Workspace, dataset_id: str) -> Optional[AbstractDataset]:
        try:
            logger.info("Fetching dataset {}.".format(dataset_id))
            return Dataset.get_by_id(workspace=workspace, id=dataset_id)
        except Exception:
            logger.info("Failed to fetch dataset {}.".format(dataset_id))
            return None

    def _get_inmem(file_path):
        logger.info("Fetching in memory data.")
        pickler = DefaultPickler()
        return pickler.load(file_path)

    def get_data(workspace: Workspace, location: str, dtype: str) -> Any:
        if dtype == "numpy" or dtype == "pandas":
            return _get_inmem(location)
        else:
            return _get_dataset(workspace, location)


# Remove this once everything uses curated envs >= 1.6.0
# from azureml.train.automl.constants import _DataArgNames
class _DataArgNames:
    X = "X"
    y = "y"
    sample_weight = "sample_weight"
    X_valid = "X_valid"
    y_valid = "y_valid"
    sample_weight_valid = "sample_weight_valid"
    training_data = "training_data"
    validation_data = "validation_data"


logger = logging.getLogger('azureml.train.automl._script')


if __name__ == '__main__':
    # Note: this file is not intended to be run manually, it is only used for submitting local managed runs
    with log_server.new_log_context():
        run = Run.get_context()
        logger.info("Starting local managed execution.")

        parser = argparse.ArgumentParser()

        parser.add_argument('--{}'.format(_DataArgNames.X), type=str,
                            dest=_DataArgNames.X)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.X), type=str,
                            dest="{}_dtype".format(_DataArgNames.X))
        parser.add_argument('--{}'.format(_DataArgNames.y), type=str,
                            dest=_DataArgNames.y)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.y), type=str,
                            dest="{}_dtype".format(_DataArgNames.y))
        parser.add_argument('--{}'.format(_DataArgNames.sample_weight), type=str,
                            dest=_DataArgNames.sample_weight)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.sample_weight), type=str,
                            dest="{}_dtype".format(_DataArgNames.sample_weight))
        parser.add_argument('--{}'.format(_DataArgNames.X_valid), type=str,
                            dest=_DataArgNames.X_valid)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.X_valid), type=str,
                            dest="{}_dtype".format(_DataArgNames.X_valid))
        parser.add_argument('--{}'.format(_DataArgNames.y_valid), type=str,
                            dest=_DataArgNames.y_valid)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.y_valid), type=str,
                            dest="{}_dtype".format(_DataArgNames.y_valid))
        parser.add_argument('--{}'.format(_DataArgNames.sample_weight_valid), type=str,
                            dest=_DataArgNames.sample_weight_valid)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.sample_weight_valid), type=str,
                            dest="{}_dtype".format(_DataArgNames.sample_weight_valid))
        parser.add_argument('--{}'.format(_DataArgNames.training_data), type=str,
                            dest=_DataArgNames.training_data)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.training_data), type=str,
                            dest="{}_dtype".format(_DataArgNames.training_data))
        parser.add_argument('--{}'.format(_DataArgNames.validation_data), type=str,
                            dest=_DataArgNames.validation_data)
        parser.add_argument('--{}-dtype'.format(_DataArgNames.validation_data), type=str,
                            dest="{}_dtype".format(_DataArgNames.validation_data))

        args = parser.parse_args()

        logger.info("Unpickling settings for local managed.")
        with open(AUTOML_SETTINGS_PATH, 'rb+') as f:
            automl_setting = pkl.load(f)
        with open(AUTOML_FIT_PARAMS_PATH, 'rb+') as f:
            fit_params = pkl.load(f)

        experiment = run.experiment
        ws = experiment.workspace

        if "show_output" in automl_setting:
            del automl_setting["show_output"]
        automl_setting['path'] = '.'
        automl_setting['debug_log'] = os.path.join(LOGS_AZUREML_DIR, 'automl.log')
        settings = AzureAutoMLSettings(experiment, **automl_setting)

        _logging.set_run_custom_dimensions(automl_settings=settings,
                                           parent_run_id=automl_setting[MANAGED_RUN_ID_PARAM],
                                           child_run_id=run.id)

        if "show_output" in fit_params:
            del fit_params["show_output"]
        fit_params["_script_run"] = run

        logger.info("Fetching data for local managed.")
        fit_params[_DataArgNames.X] = \
            get_data(workspace=ws, location=args.X, dtype=args.X_dtype)
        fit_params[_DataArgNames.y] = \
            get_data(workspace=ws, location=args.y, dtype=args.y_dtype)
        fit_params[_DataArgNames.sample_weight] = \
            get_data(workspace=ws, location=args.sample_weight, dtype=args.sample_weight_dtype)
        fit_params[_DataArgNames.X_valid] = \
            get_data(workspace=ws, location=args.X_valid, dtype=args.X_valid_dtype)
        fit_params[_DataArgNames.y_valid] = \
            get_data(workspace=ws, location=args.y_valid, dtype=args.y_valid_dtype)
        fit_params[_DataArgNames.sample_weight_valid] = \
            get_data(workspace=ws, location=args.sample_weight_valid, dtype=args.sample_weight_valid_dtype)
        fit_params[_DataArgNames.training_data] = \
            get_data(workspace=ws, location=args.training_data, dtype=args.training_data_dtype)
        fit_params[_DataArgNames.validation_data] = \
            get_data(workspace=ws, location=args.validation_data, dtype=args.validation_data_dtype)

        automl_estimator = AzureAutoMLClient(experiment, settings)

        logger.info("Starting a local legacy fit inside local managed scenario.")
        local_run = automl_estimator.fit(**fit_params)
