# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml._common._error_definition import error_decorator
from azureml._common._error_definition.system_error import ClientError
from azureml._common._error_definition.user_error import (
    ArgumentBlankOrEmpty, ArgumentInvalid, ArgumentMismatch, ArgumentOutOfRange, Authentication, BadData, BadArgument,
    ConnectionFailure, InvalidDimension, MalformedArgument, Memory, NotFound, NotReady, NotSupported, Timeout,
    EmptyData)

from azureml.automl.core.shared._diagnostics.error_strings import AutoMLErrorStrings


# region ArgumentBlankOrEmpty
@error_decorator(use_parent_error_code=True)
class FeaturizationConfigEmptyFillValue(ArgumentBlankOrEmpty):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_EMPTY_FILL_VALUE
# endregion


# region ArgumentInvalid
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_TYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentWithSupportedValues(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_WITH_SUPPORTED_VALUES


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentWithSupportedValuesForTask(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_WITH_SUPPORTED_VALUES_FOR_TASK


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentForTask(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_FOR_TASK


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class TensorflowAlgosAllowedButDisabled(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TENSORFLOW_ALGOS_ALLOWED_BUT_DISABLED


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidCVSplits(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_CV_SPLITS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidInputDatatype(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_INPUT_DATATYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InputDataWithMixedType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INPUT_DATA_WITH_MIXED_TYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class AllAlgorithmsAreBlocked(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALL_ALGORITHMS_ARE_BLOCKED


@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class InvalidComputeTargetForDatabricks(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_COMPUTE_TARGET_FOR_DATABRICKS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class EmptyLagsForColumns(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.EMPTY_LAGS_FOR_COLUMNS


@error_decorator(use_parent_error_code=True)
class TimeseriesInvalidDateOffsetType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_INVALID_DATE_OFFSET_TYPE


@error_decorator(use_parent_error_code=True)
class OnnxNotEnabled(ArgumentInvalid):
    @property
    def message_format(self):
        return AutoMLErrorStrings.ONNX_NOT_ENABLED


@error_decorator(use_parent_error_code=True)
class OnnxSplitsNotEnabled(ArgumentInvalid):
    @property
    def message_format(self):
        return AutoMLErrorStrings.ONNX_SPLITS_NOT_ENABLED
# endregion


# region ArgumentMismatch
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class AllowedModelsSubsetOfBlockedModels(ArgumentMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALLOWED_MODELS_SUBSET_OF_BLOCKED_MODELS


@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class ConflictingValueForArguments(ArgumentMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONFLICTING_VALUE_FOR_ARGUMENTS


@error_decorator(use_parent_error_code=True)
class InvalidDampingSettings(ConflictingValueForArguments):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_DAMPING_SETTINGS


@error_decorator(use_parent_error_code=True)
class ConflictingFeaturizationConfigDroppedColumns(ConflictingValueForArguments):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONFLICTING_FEATURIZATION_CONFIG_DROPPED_COLUMNS


@error_decorator(use_parent_error_code=True)
class ConflictingFeaturizationConfigReservedColumns(ConflictingValueForArguments):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONFLICTING_FEATURIZATION_CONFIG_RESERVED_COLUMNS
# endregion


# region BadArgument
@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class InvalidFeaturizer(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_FEATURIZER


@error_decorator(use_parent_error_code=True)
class InvalidSTLFeaturizerForMultiplicativeModel(InvalidFeaturizer):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_STL_FEATURIZER_FOR_MULTIPLICATIVE_MODEL


@error_decorator(use_parent_error_code=True)
class FeaturizationConfigParamOverridden(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_PARAM_OVERRIDDEN


@error_decorator(use_parent_error_code=True)
class FeaturizationConfigMultipleImputers(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_MULTIPLE_IMPUTERS


class MissingColumnsInData(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.MISSING_COLUMNS_IN_DATA


@error_decorator(use_parent_error_code=True)
class FeaturizationConfigColumnMissing(MissingColumnsInData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_COLUMN_MISSING


@error_decorator(use_parent_error_code=True)
class GrainContainsEmptyValues(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_NAN_GRAIN_VALUES
# endregion


# region ArgumentOutOfRange
@error_decorator(use_parent_error_code=True)
class NCrossValidationsExceedsTrainingRows(ArgumentOutOfRange):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.N_CROSS_VALIDATIONS_EXCEEDS_TRAINING_ROWS


@error_decorator(use_parent_error_code=True)
class ExperimentTimeoutForDataSize(ArgumentOutOfRange):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.EXPERIMENT_TIMEOUT_FOR_DATA_SIZE


@error_decorator(use_parent_error_code=True)
class QuantileRange(ArgumentOutOfRange):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.QUANTILE_RANGE
# endregion


# region MalformedArgument
class MalformedJsonString(MalformedArgument):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MALFORMED_JSON_STRING
# endregion


# region NotReady
class ComputeNotReady(NotReady):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.COMPUTE_NOT_READY
# endregion


# region NotFound
class MethodNotFound(NotFound):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.METHOD_NOT_FOUND


class DatastoreNotFound(NotFound):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASTORE_NOT_FOUND


class DataPathNotFound(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_PATH_NOT_FOUND


class MissingSecrets(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MISSING_SECRETS


@error_decorator(use_parent_error_code=True)
class NoMetricsData(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.NO_METRICS_DATA


class ModelMissing(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MODEL_MISSING
# endregion


# region NotSupported
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class LargeDataAlgorithmsWithUnsupportedArguments(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.LARGE_DATA_ALGORITHMS_WITH_UNSUPPORTED_ARGUMENTS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class FeatureUnsupportedForIncompatibleArguments(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURE_UNSUPPORTED_FOR_INCOMPATIBLE_ARGUMENTS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class NonDnnTextFeaturizationUnsupported(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.NON_DNN_TEXT_FEATURIZATION_UNSUPPORTED


class InvalidOperationOnRunState(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_OPERATION_ON_RUN_STATE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class FeaturizationConfigForecastingStrategy(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURIZATION_CONFIG_FORECASTING_STRATEGY


class RemoteInferenceUnsupported(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.REMOTE_INFERENCE_UNSUPPORTED


# A package is either missing or has an incompatible version installed.
class IncompatibleOrMissingDependency(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INCOMPATIBLE_OR_MISSING_DEPENDENCY


# Snapshot is either larger than 300MB or exceeds max allowed files.
@error_decorator(use_parent_error_code=False, details_uri="http://aka.ms/aml-largefiles")
class SnapshotLimitExceeded(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.SNAPSHOT_LIMIT_EXCEED
# endregion


# region InvalidDimension
class DatasetsFeatureCountMismatch(InvalidDimension):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASETS_FEATURE_COUNT_MISMATCH
# endregion


# region BadData
class AllTargetsUnique(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALL_TARGETS_UNIQUE


class AllTargetsOverlapping(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALL_TARGETS_OVERLAPPING


@error_decorator(details_uri="https://aka.ms/datasetfromdelimitedfiles")
class InconsistentNumberOfSamples(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INCONSISTENT_NUMBER_OF_SAMPLES


class PandasDatetimeConversion(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.PANDAS_DATETIME_CONVERSION_ERROR


class TimeseriesColumnNamesOverlap(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_COLUMN_NAMES_OVERLAP


class TimeseriesTypeMismatchFullCV(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_TYPE_MISMATCH_FULL_CV


class TimeseriesDfContainsNaN(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_DF_CONTAINS_NAN


class TimeseriesNoDataContext(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_NO_DATA_CONTEXT


class TimeseriesNothingToPredict(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_NOTHING_TO_PREDICT


class TimeseriesNonContiguousTargetColumn(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_NON_CONTIGUOUS_TARGET_COLUMN


class TimeseriesMissingValuesInY(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.TIMESERIES_MISSING_VALUES_IN_Y


class TransformerYMinGreater(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TRANSFORMER_Y_MIN_GREATER


class TooManyLabels(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TOO_MANY_LABELS


class BadDataInWeightColumn(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.BAD_DATA_IN_WEIGHT_COLUMN


class NoFeatureTransformationsAdded(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.NO_FEATURE_TRANSFORMATIONS_ADDED


@error_decorator(use_parent_error_code=True)
class PowerTransformerInverseTransform(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.POWER_TRANSFORMER_INVERSE_TRANSFORM


class MaxHorizonExceeded(BadData):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MAX_HORIZON_EXCEEDED


class ContentModified(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONTENT_MODIFIED
# endregion


# region EmptyData
class InputDatasetEmpty(EmptyData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INPUT_DATASET_EMPTY
# endregion


# region Authentication
class DataPathInaccessible(Authentication):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_PATH_INACCESSIBLE
# endregion


# region ClientError
@error_decorator(details_uri="https://docs.microsoft.com/en-us/azure/machine-learning/"
                             "resource-known-issues#automated-machine-learning")
class AutoMLInternal(ClientError):
    """Base class for all AutoML system errors."""
    @property
    def message_format(self):
        return AutoMLErrorStrings.AUTOML_INTERNAL


class Data(AutoMLInternal):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA


class Service(AutoMLInternal):
    @property
    def message_format(self):
        return AutoMLErrorStrings.SERVICE
# endregion


# region Memory
class Memorylimit(Memory):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_MEMORY_ERROR


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/azurevmsizes")
class InsufficientMemory(Memory):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INSUFFICIENT_MEMORY


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/azurevmsizes")
class InsufficientMemoryWithHeuristics(Memory):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INSUFFICIENT_MEMORY_WITH_HEURISTICS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/azurevmsizes")
class InsufficientMemoryLikely(Memory):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INSUFFICIENT_MEMORY_LIKELY
# endregion


# region Timeout
@error_decorator(is_transient=True, details_uri="https://aka.ms/storageoptimization")
class DatasetFileRead(Timeout):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASET_FILE_READ
# endregion


# region ConnectionFailure
@error_decorator(use_parent_error_code=True, is_transient=True)
class HttpConnectionFailure(ConnectionFailure):
    @property
    def message_format(self):
        return AutoMLErrorStrings.HTTP_CONNECTION_FAILURE
# endregion
