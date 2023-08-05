# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with AutoMLConfig."""
from typing import Any, cast, Callable, Dict, List, Optional, Set, Tuple, Union

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ConflictingValueForArguments
from azureml.automl.core.shared.exceptions import DataException, ConfigException, EmptyDataException


def _check_validation_config(
    X_valid: Any,
    y_valid: Any,
    sample_weight: Any,
    sample_weight_valid: Any,
    cv_splits_indices: Any,
    n_cross_validations: Optional[int] = None,
    validation_size: Optional[float] = None
) -> None:
    """
    Validate that validation parameters have been correctly provided.

    :param X_valid:
    :param y_valid:
    :param sample_weight:
    :param sample_weight_valid:
    :param cv_splits_indices:
    :param n_cross_validations:
    :param validation_size:
    """

    if X_valid is not None and y_valid is None:
        raise EmptyDataException(
            "X validation provided but y validation data is missing.", has_pii=False)

    if y_valid is not None and X_valid is None:
        raise EmptyDataException(
            "y validation provided but X validation data is missing.", has_pii=False)

    if X_valid is not None and sample_weight is not None and \
            sample_weight_valid is None:
        raise EmptyDataException("sample_weight_valid should be set to a valid value", has_pii=False)

    if sample_weight_valid is not None and X_valid is None:
        raise EmptyDataException(
            "sample_weight_valid should only be set if X_valid is set", has_pii=False)

    if X_valid is not None:
        if n_cross_validations is not None and n_cross_validations > 0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="n_cross_validations",
                    arguments=', '.join(['validation_data/X_valid', 'n_cross_validations'])
                )
            )
        if validation_size is not None and validation_size > 0.0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="validation_size",
                    arguments=', '.join(['validation_data/X_valid', 'validation_size'])
                )
            )

    if cv_splits_indices is not None:
        if n_cross_validations is not None and n_cross_validations > 0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="cv_splits_indices",
                    arguments=', '.join(['cv_splits_indices', 'n_cross_validations'])
                )
            )
        if validation_size is not None and validation_size > 0.0:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="cv_splits_indices",
                    arguments=', '.join(['cv_splits_indices', 'validation_size'])
                )
            )
        if X_valid is not None:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="cv_splits_indices",
                    arguments=', '.join(['cv_splits_indices', 'validation_data/X_valid'])
                )
            )
