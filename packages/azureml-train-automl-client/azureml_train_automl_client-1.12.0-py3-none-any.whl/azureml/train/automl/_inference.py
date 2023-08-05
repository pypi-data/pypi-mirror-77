# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import argparse
import io
import logging
import os
import pickle as pkl
import sys
import tempfile
from typing import Any, TYPE_CHECKING

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared.exceptions import MemorylimitException
from azureml.core import Run, Workspace
from azureml.data.abstract_dataset import AbstractDataset
from azureml.train.automl._constants_azureml import MODEL_PATH
from azureml.train.automl.constants import LOCAL_MODEL_PATH, INFERENCE_OUTPUT

try:
    from azureml.train.automl.model_proxy import RESULTS_PROPERTY
    from azureml.automl.core.shared._diagnostics.automl_error_definitions import Memorylimit
    from azureml.train.automl._local_managed_utils import get_data
except ImportError:
    if not TYPE_CHECKING:
        # remove all of these once 1.11.0 curated envs roll out
        RESULTS_PROPERTY = "inference_results"
        from azureml._common._error_definition.user_error import Memory
        from azureml.automl.core.shared.pickler import DefaultPickler
        from azureml.core import Dataset

        class Memorylimit(Memory):
            @property
            def message_format(self):
                return "Failed to retrieve data from {data} due to MemoryError."

        def _get_dataset(workspace, dataset_id):
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

logger = logging.getLogger(__name__)


def _get_memory_safe_data(data, data_name="unknown"):
    if isinstance(data, AbstractDataset):
        try:
            return data.to_pandas_dataframe()
        except MemoryError as e:
            raise MemorylimitException(azureml_error=AzureMLError.create(Memorylimit, data=type(data)),
                                       inner_exception=e, target=data_name)
    else:
        return data


def _get_pandas(results):
    if results is None:
        raise Exception("Inferencing returned no results.")
    elif isinstance(results, pd.DataFrame):
        logger.info("Inference output as pandas.")
        return results
    elif isinstance(results, AbstractDataset):
        logger.info("Inference output as AbstractDataset, casting to pandas.")
        return results.to_pandas_dataframe()
    else:
        # if its not any of the above types, assume its some primitive array type that pandas can accept
        logger.info("Inference output is not pandas or AbstractDataset, casting to pandas.")
        return pd.DataFrame(results)


def _save_results(results, run):
    logger.info("Saving results.")

    if isinstance(results, tuple) or isinstance(results, list):
        logger.info("Multiple inference outputs, casting to pandas.")
        results_pd = [_get_pandas(result) for result in results]
    else:
        logger.info("Single inference output, casting to pandas.")
        results_pd = [_get_pandas(results)]

    with tempfile.TemporaryDirectory() as project_folder:
        results_locations = []
        for i, dataset in enumerate(results_pd):
            file_name = INFERENCE_OUTPUT.format(i)
            results_data_fname = os.path.join(project_folder, file_name)

            dataset.to_csv(results_data_fname, index=False)

            logger.info("Uploading results to {}".format(args.inference_results_path))
            datastore = run.experiment.workspace.get_default_datastore()
            datastore.upload(src_dir=project_folder, target_path=args.inference_results_path.format(i), overwrite=True)
            results_locations.append(args.inference_results_path.format(i))
    run.add_properties({RESULTS_PROPERTY: results_locations})


if __name__ == '__main__':
    logger.info("Starting inference run.")
    # pandas is only available on the remote compute, we don't want this imported in azureml-train-automl-client
    import pandas as pd

    run = Run.get_context()

    parser = argparse.ArgumentParser()

    # the run id of he child run we want to inference
    parser.add_argument('--child_run_id', type=str, dest='child_run_id')
    # Which function we want to use for inferencing, "predict", "forecast", or "predict_proba"
    parser.add_argument('--function_name', type=str, dest='function_name')
    # The Dataset path to upload the inference results to.
    parser.add_argument('--inference_results_path', type=str, dest='inference_results_path')

    # Parameters for x and y values
    parser.add_argument('--values', type=str, dest='values')
    parser.add_argument('--values-dtype', type=str, dest='values_dtype')
    parser.add_argument('--y_values', type=str, dest='y_values')
    parser.add_argument('--y_values-dtype', type=str, dest='y_values_dtype')

    args = parser.parse_args()

    X_inputs = get_data(workspace=run.experiment.workspace, location=args.values, dtype=args.values_dtype)
    y_inputs = get_data(workspace=run.experiment.workspace, location=args.y_values, dtype=args.y_values_dtype)

    logger.info("Running {} for run {}.".format(args.child_run_id, args.function_name))

    logger.info("Fetching model.")

    child_run = Run(run.experiment, args.child_run_id)

    child_run.download_file(name=MODEL_PATH, output_file_path=LOCAL_MODEL_PATH)

    logger.info("Loading model.")
    with open(LOCAL_MODEL_PATH, "rb") as model_file:
        fitted_model = pkl.load(model_file)

    X_inputs = _get_memory_safe_data(X_inputs, "X")
    y_inputs = _get_memory_safe_data(y_inputs, "y")

    logger.info("Inferencing.")
    inference_func = getattr(fitted_model, args.function_name)
    try:
        if y_inputs is None:
            results = inference_func(X_inputs)
        else:
            results = inference_func(X_inputs, y_inputs)
    except MemoryError as e:
        generic_msg = 'Failed to {} due to MemoryError'.format(args.function_name)
        raise MemorylimitException.from_exception(e, msg=generic_msg, has_pii=False)
    except Exception as e:
        logger.info("Failed to inference the model.")
        raise

    _save_results(results, run)
