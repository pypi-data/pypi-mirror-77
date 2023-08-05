# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with azureml.dataprep."""
from typing import Any, Dict, Optional
import json

from azureml.automl.core.shared.exceptions import DataFormatException, DataprepException

DATAPREP_INSTALLED = True
try:
    import azureml.dataprep as dprep
except ImportError:
    DATAPREP_INSTALLED = False
try:
    from dprep.api.dataflow import Dataflow
except ImportError:
    Dataflow = Any


__activities_flag__ = 'activities'


def get_dataprep_json(X: Optional[Dataflow] = None,
                      y: Optional[Dataflow] = None,
                      sample_weight: Optional[Dataflow] = None,
                      X_valid: Optional[Dataflow] = None,
                      y_valid: Optional[Dataflow] = None,
                      sample_weight_valid: Optional[Dataflow] = None,
                      cv_splits_indices: Optional[Dataflow] = None) -> Optional[str]:
    """Get dataprep json.

    :param X: Training features.
    :type X: azureml.dataprep.Dataflow
    :param y: Training labels.
    :type y: azureml.dataprep.Dataflow
    :param sample_weight: Sample weights for training data.
    :type sample_weight: azureml.dataprep.Dataflow
    :param X_valid: validation features.
    :type X_valid: azureml.dataprep.Dataflow
    :param y_valid: validation labels.
    :type y_valid: azureml.dataprep.Dataflow
    :param sample_weight_valid: validation set sample weights.
    :type sample_weight_valid: azureml.dataprep.Dataflow
    :param cv_splits_indices: custom validation splits indices.
    :type cv_splits_indices: azureml.dataprep.Dataflow
    return: JSON string representation of a dict of Dataflows
    """
    dataprep_json = None
    df_value_list = [X, y, sample_weight, X_valid,
                     y_valid, sample_weight_valid, cv_splits_indices]
    if any(var is not None for var in df_value_list):
        def raise_type_error():
            raise DataFormatException("Passing X, y, sample_weight, X_valid, y_valid, sample_weight_valid or "
                                      "cv_splits_indices as Pandas or numpy dataframe is only supported for local "
                                      "runs. For remote runs, please provide X, y, sample_weight, X_valid, y_valid, "
                                      "sample_weight_valid and cv_splits_indices as azureml.dataprep.Dataflow "
                                      "objects, or provide a get_data() file instead.", has_pii=False)

        dataflow_dict = {
            'X': X,
            'y': y,
            'sample_weight': sample_weight,
            'X_valid': X_valid,
            'y_valid': y_valid,
            'sample_weight_valid': sample_weight_valid
        }
        if cv_splits_indices is not None:
            for i in range(len(cv_splits_indices or [])):
                split = cv_splits_indices[i]
                if not is_dataflow(split):
                    raise_type_error()
                else:
                    dataflow_dict['cv_splits_indices_{0}'.format(i)] = split
        dataprep_json = save_dataflows_to_json(dataflow_dict)
        if dataprep_json is None:
            raise_type_error()

    return dataprep_json


def get_dataprep_json_dataset(training_data: Optional[Dataflow] = None,
                              validation_data: Optional[Dataflow] = None) -> Optional[str]:
    """Get dataprep json.

    :param training_data: Training data.
    :type training_data: azureml.dataprep.Dataflow
    :param validation_data: Validation data
    :type validation_data: azureml.dataprep.Dataflow
    return: JSON string representation of a dict of Dataflows
    """
    dataprep_json = None
    df_value_list = [training_data, validation_data]
    if any(var is not None for var in df_value_list):
        dataflow_dict = {
            'training_data': training_data,
            'validation_data': validation_data
        }
        dataprep_json = save_dataflows_to_json(dataflow_dict)
        if dataprep_json is None:
            raise DataFormatException("Passing X, y, sample_weight, X_valid, y_valid, sample_weight_valid or "
                                      "cv_splits_indices as numpy or Pandas dataframe is only supported for "
                                      "non-streaming runs. For streaming runs, please provide 'training_data' and "
                                      "'validation_data' as azureml.dataprep.Dataflow objects.", has_pii=False)

    return dataprep_json


def save_dataflows_to_json(dataflow_dict: Dict[str, Dataflow]) -> Optional[str]:
    """Save dataflows to json.

    Param dataflow_dict: the dict with key as dataflow name and value as dataflow
    type: dict(str, azureml.dataprep.Dataflow)
    return: the JSON string representation of a dict of Dataflows
    """
    dataflow_json_dict = {}     # type: Dict[str, Any]
    for name in dataflow_dict:
        dataflow = dataflow_dict[name]
        if not is_dataflow(dataflow):
            continue
        try:
            # json.dumps(json.loads(...)) to remove newlines and indents
            dataflow_json = json.dumps(json.loads(dataflow.to_json()))
        except Exception as e:
            raise DataprepException.from_exception(e).with_generic_msg('Error when saving dataflows to JSON.')
        dataflow_json_dict[name] = dataflow_json

    if len(dataflow_json_dict) == 0:
        return None

    dataflow_json_dict[__activities_flag__] = 0  # backward compatible with old Jasmine
    return json.dumps(dataflow_json_dict)


def load_dataflows_from_json_dict(dataflow_json_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Load dataflows from json dict.

    Param dataprep_json: the JSON string representation of a dict of Dataflows
    type: str
    return: a dict with key as dataflow name and value as dataflow, or None if JSON is malformed
    """
    if __activities_flag__ in dataflow_json_dict:
        del dataflow_json_dict[__activities_flag__]  # backward compatible with old Jasmine

    dataflow_dict = {}
    for name in dataflow_json_dict:
        try:
            dataflow = dprep.Dataflow.from_json(dataflow_json_dict[name])
        except Exception as e:
            raise DataprepException.from_exception(e)
        dataflow_dict[name] = dataflow
    return dataflow_dict


def is_dataflow(dataflow: Dataflow) -> bool:
    """Check if object passed is of type dataflow.

    Param dataflow:
    return: True if dataflow is of type azureml.dataprep.Dataflow
    """
    if not DATAPREP_INSTALLED or not isinstance(dataflow, dprep.Dataflow):
        return False
    return True
