# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


class AutoMLErrorStrings:
    """
    All un-formatted error strings that accompany the common error codes in AutoML.

    Dev note: Please keep this list sorted on keys.
    """

    # region UserErrorStrings
    ALLOWED_MODELS_SUBSET_OF_BLOCKED_MODELS = "All allowed models are within blocked models list. Please " \
                                              "remove models from the exclude list or add models to the allow list."
    ALLOWED_MODELS_UNSUPPORTED = "Allowed models [{allowed_models}] are not supported for scenario: " \
                                 "{scenario}."
    ALL_ALGORITHMS_ARE_BLOCKED = "All models are blocked. Please ensure that at least one model is allowed."
    ALL_TARGETS_OVERLAPPING = "At least two distinct values for the target column are required for " \
                              "{task_type} task. Please check the label values."
    ALL_TARGETS_UNIQUE = "For a {task_type} task, the label cannot be unique for every sample."
    BAD_DATA_IN_WEIGHT_COLUMN = "Weight column contains invalid values such as 'NaN' or 'infinite'"
    COMPUTE_NOT_READY = "Compute not in 'Succeeded' state. Please choose another compute or wait till it is ready."
    CONFLICTING_FEATURIZATION_CONFIG_DROPPED_COLUMNS = "Featurization '{sub_config_name}' customization contains " \
                                                       "columns ({dropped_columns}), which are also configured to be" \
                                                       " dropped via drop_columns. Please resolve the inconsistency " \
                                                       "by reconfiguring the columns that are to be customized."
    CONFLICTING_FEATURIZATION_CONFIG_RESERVED_COLUMNS = "Featurization '{sub_config_name}' customization contains " \
                                                        "reserved columns ({reserved_columns}). Please resolve the " \
                                                        "inconsistency by reconfiguring the columns that are to be " \
                                                        "customized."
    CONFLICTING_VALUE_FOR_ARGUMENTS = "Conflicting or duplicate values are provided for arguments: [{arguments}]"
    CONTENT_MODIFIED = "The data was modified while being read. Error: {dprep_error}"
    DATASETS_FEATURE_COUNT_MISMATCH = "The number of features in [{first_dataset_name}]({first_dataset_shape}) does " \
                                      "not match with those in [{second_dataset_name}]({second_dataset_shape}). " \
                                      "Please inspect your data, and make sure that features are aligned in " \
                                      "both the Datasets."
    DATASET_FILE_READ = "Fetching data from the underlying storage account timed out. Please retry again after " \
                        "some time, or optimize your blob storage performance."
    DATASTORE_NOT_FOUND = "The provided Datastore was not found. Error: {dprep_error}"
    DATA_MEMORY_ERROR = "Failed to retrieve data from {data} due to MemoryError."
    DATA_PATH_INACCESSIBLE = "The provided path to the data in the Datastore was inaccessible. Please make sure " \
                             "you have the necessary access rights on the resource. Error: {dprep_error}"
    DATA_PATH_NOT_FOUND = "The provided path to the data in the Datastore does not exist. Error: {dprep_error}"
    EMPTY_LAGS_FOR_COLUMNS = "The lags for all columns are represented by empty lists. Please set the " \
                             "target_lags parameter to None to turn off the lag feature and run the experiment again."
    EXPERIMENT_TIMEOUT_FOR_DATA_SIZE = "The ExperimentTimeout should be set more than {minimum} minutes with an " \
                                       "input data of rows*cols({rows}*{columns}={total}), and up to {maximum}."
    FEATURE_UNSUPPORTED_FOR_INCOMPATIBLE_ARGUMENTS = "Feature [{feature_name}] is unsupported due to incompatible " \
                                                     "values for argument(s): [{arguments}]"
    FEATURIZATION_CONFIG_COLUMN_MISSING = "The column(s) '{columns}' specified in the Featurization " \
                                          "{sub_config_name} customization is not present in the data frame. " \
                                          "Valid columns: {all_columns}"
    FEATURIZATION_CONFIG_EMPTY_FILL_VALUE = "A fill value is required for constant value imputation. Please provide " \
                                            "a non-empty value for '{argument_name}' parameter. Example code: " \
                                            "`featurization_config.add_transformer_params('Imputer', ['column_name']" \
                                            ", \"{{'strategy': 'constant', 'fill_value': 0}}\")`"
    FEATURIZATION_CONFIG_FORECASTING_STRATEGY = "Only the following strategies are enabled for a " \
                                                "Forecasting task's target column: ({strategies}). Please fix your " \
                                                "featurization configuration and try again."
    FEATURIZATION_CONFIG_MULTIPLE_IMPUTERS = "Only one imputation method may be defined for each column. In the " \
                                             "provided configuration, multiple imputers are assigned to the " \
                                             "following columns {columns}\n. Please verify that only one imputer " \
                                             "is defined per column."
    FEATURIZATION_CONFIG_PARAM_OVERRIDDEN = "Failed while {stage} learned transformations. This could be caused by " \
                                            "transformer parameters being overridden. Please check logs for " \
                                            "detailed error messages."
    HTTP_CONNECTION_FAILURE = "Failed to establish HTTP connection to the service. This may be caused due the local " \
                              "compute being overwhelmed with HTTP requests. Please make sure that there are " \
                              "enough network resources available for the experiment to run. More details: " \
                              "{error_details}"
    INCOMPATIBLE_OR_MISSING_DEPENDENCY = "Please install specific versions of packages: {missing_packages_message}"
    INCONSISTENT_NUMBER_OF_SAMPLES = "The number of samples in {data_one} and {data_two} are inconsistent. If you " \
                                     "are using an AzureML Dataset as input, this may be caused as a result of " \
                                     "having multi-line strings in the data. Please make sure that " \
                                     "'support_multi_line' is set to True when creating a Dataset. Example: " \
                                     "Dataset.Tabular.from_delimited_files('http://path/to/csv', " \
                                     "support_multi_line = True)"
    INPUT_DATASET_EMPTY = "The provided Dataset contained no data. Please make sure there are non-zero number " \
                          "of samples and features in the data."
    INPUT_DATA_WITH_MIXED_TYPE = "A mix of Dataset and Pandas objects provided. " \
                                 "Please provide either all Dataset or all Pandas objects."
    INSUFFICIENT_MEMORY = "There is not enough memory on the machine to do the requested operation. " \
                          "Please try running the experiment on a VM with higher memory."
    INSUFFICIENT_MEMORY_LIKELY = "'Subprocess (pid {pid}) killed by unhandled signal {errorcode} ({errorname}). " \
                                 "This is most likely due to an out of memory condition. " \
                                 "Please try running the experiment on a VM with higher memory."
    INSUFFICIENT_MEMORY_WITH_HEURISTICS = "There is not enough memory on the machine to do the requested operation. " \
                                          "The amount of available memory is {avail_mem} out of {total_mem} total " \
                                          "memory. To fit the model at least {min_mem} more memory is required. " \
                                          "Please try running the experiment on a VM with higher memory."
    INVALID_ARGUMENT_FOR_TASK = "Invalid argument(s) '{arguments}' for task type '{task_type}'."
    INVALID_ARGUMENT_TYPE = "Argument [{argument}] is of unsupported type: [{actual_type}]. " \
                            "Supported type(s): [{expected_types}]"
    INVALID_ARGUMENT_WITH_SUPPORTED_VALUES = "Invalid argument(s) '{arguments}' specified. " \
                                             "Supported value(s): '{supported_values}'."
    INVALID_ARGUMENT_WITH_SUPPORTED_VALUES_FOR_TASK = "Invalid argument(s) '{arguments}' specified for task type " \
                                                      "'{task_type}'. Supported value(s): '{supported_values}'."
    INVALID_COMPUTE_TARGET_FOR_DATABRICKS = "Databricks compute cannot be directly attached for AutoML runs. " \
                                            "Please pass in a spark context instead using the spark_context " \
                                            "parameter and set compute_target to 'local'."
    INVALID_CV_SPLITS = "cv_splits_indices should be a List of List[numpy.ndarray]. \
                            Each List[numpy.ndarray] corresponds to a CV fold and should have just 2 elements: " \
                        "The indices for training set and for the validation set."
    INVALID_DAMPING_SETTINGS = "Conflicting values are provided for arguments [{model_type}] and [{is_damped}]. " \
                               "Damping can only be applied when there is a trend term."
    INVALID_FEATURIZER = "[{featurizer_name}] is not a valid featurizer for featurizer type: [{featurizer_type}]"
    INVALID_INPUT_DATATYPE = "Input of type '{input_type}' is not supported. Supported types: [{supported_types}]"
    INVALID_OPERATION_ON_RUN_STATE = "Operation [{operation_name}] on the RunID [{run_id}] is invalid. " \
                                     "Current run state: [{run_state}]"
    INVALID_STL_FEATURIZER_FOR_MULTIPLICATIVE_MODEL = "Cannot use multiplicative model type [{model_type}] because " \
                                                      "trend contains negative or zero values."
    LARGE_DATA_ALGORITHMS_WITH_UNSUPPORTED_ARGUMENTS = "AveragedPerceptronClassifier, FastLinearRegressor, " \
                                                       "OnlineGradientDescentRegressor are incompatible with " \
                                                       "following arguments: X, " \
                                                       "n_cross_validations, enable_dnn, " \
                                                       "enable_onnx_compatible_models, enable_subsampling, " \
                                                       "task_type=forecasting, spark_context and local compute"
    MALFORMED_JSON_STRING = "Failed to parse the provided JSON string. Error: {json_decode_error}"
    MAX_HORIZON_EXCEEDED = "Input prediction data X_pred or input forecast_destination contains dates later than " \
                           "maximum forecast horizon. Please shorten the prediction data so that it is within the " \
                           "maximum horizon or adjust the forecast_destination date."
    MEMORY_EXHAUSTED = "There is not enough memory on the machine to fit the model. " \
                       "The amount of available memory is {avail_mem} out of {total_mem} " \
                       "total memory. To fit the model at least {min_mem} more memory is required. " \
                       "Please install more memory or use bigger virtual " \
                       "machine to generate model on this data set."
    METHOD_NOT_FOUND = "Required method [{method_name}] is not found."
    MISSING_COLUMNS_IN_DATA = "Expected column(s) {columns} not found in {data_object_name}"
    MISSING_SECRETS = "Failed to get data from the Datastore due to missing secrets. Error: {dprep_error}"
    MODEL_MISSING = "Could not find a model with valid score for metric '{metric}'. Please ensure that at least one " \
                    "run was successfully completed with a valid score for the given metric."
    NON_DNN_TEXT_FEATURIZATION_UNSUPPORTED = "For non-English pre-processing of text data, please set " \
                                             "enable_dnn=True and make sure you are using GPU compute."
    NO_FEATURE_TRANSFORMATIONS_ADDED = "No features could be identified or generated for the given data. " \
                                       "Please pre-process the data manually, or provide custom featurization options."
    NO_METRICS_DATA = "No metrics related data was present at the time of \'{metric}\' calculation either because " \
                      "data was not uploaded in time or because no runs were found in completed state. " \
                      "If the former, please try again in a few minutes."
    N_CROSS_VALIDATIONS_EXCEEDS_TRAINING_ROWS = "Number of training rows ({training_rows}) is less than total " \
                                                "requested CV splits ({n_cross_validations}). " \
                                                "Please reduce the number of splits requested."
    ONNX_NOT_ENABLED = "Requested an ONNX compatible model but the run has ONNX compatibility disabled."
    ONNX_SPLITS_NOT_ENABLED = "Requested a split ONNX featurized model but the run has split ONNX feautrization " \
                              "disabled."
    PANDAS_DATETIME_CONVERSION_ERROR = "Column {column} of type {column_type} cannot be converted to pandas datetime."
    POWER_TRANSFORMER_INVERSE_TRANSFORM = "Failed to inverse transform: y_min is greater than the observed minimum " \
                                          "in y."
    QUANTILE_RANGE = "Value for argument quantile ({quantile}) is out of range. Quantiles must be strictly " \
                     "greater than 0 and less than 1."
    REMOTE_INFERENCE_UNSUPPORTED = "Remote inference is not supported for local or ADB runs."
    SNAPSHOT_LIMIT_EXCEED = "Snapshot is either large than {size} MB or {files} files"
    TENSORFLOW_ALGOS_ALLOWED_BUT_DISABLED = "Tensorflow isn't enabled but only Tensorflow models were specified in " \
                                            "allowed_models."
    TIMESERIES_COLUMN_NAMES_OVERLAP = "Some of the columns that are about to be created by LagLeadOperator already " \
                                      "exist in the input TimeSeriesDataFrame: [{column_names}. Please set " \
                                      "`overwrite_columns` to `True` to proceed anyways."
    TIMESERIES_DF_CONTAINS_NAN = "One of X_pred columns contains only NaNs. If it is expected, please run forecast()" \
                                 " with ignore_data_errors=True."
    TIMESERIES_INVALID_DATE_OFFSET_TYPE = "The data set frequency must be a string or None. The string must " \
                                          "represent a pandas date offset. Please refer to pandas documentation on " \
                                          "date offsets: {pandas_url}"
    TIMESERIES_MISSING_VALUES_IN_Y = "All of the values in y_pred are NA or missing. At least one value of " \
                                     "y_pred should not be NA or missing."
    TIMESERIES_NAN_GRAIN_VALUES = "The time series identifier {time_series_id} contains empty values. " \
                                  "Please fill these values and run the AutoML job again."
    TIMESERIES_NON_CONTIGUOUS_TARGET_COLUMN = "The y values contain non-contiguous NaN values. If it is expected, " \
                                              "please run forecast() with ignore_data_errors=True. In this case the " \
                                              "NaNs before the time-wise latest NaNs will be imputed."
    TIMESERIES_NOTHING_TO_PREDICT = "Actual values are present for all times in the input data frame - there is " \
                                    "nothing to forecast. Please set 'y' values to np.NaN for times where you " \
                                    "need a forecast."
    TIMESERIES_NO_DATA_CONTEXT = "No y values were provided. We expected non-null target values as prediction " \
                                 "context because there is a gap between train and test and the forecaster depends " \
                                 "on previous values of target. If it is expected, please run forecast() with " \
                                 "ignore_data_errors=True. In this case the values in the gap will be imputed."
    TIMESERIES_TYPE_MISMATCH_FULL_CV = "Detected multiple types for columns {columns}. Please set " \
                                       "FeaturizationConfig.column_purposes to force consistent types."
    TOO_MANY_LABELS = "Found more than 2,147,483,647 labels. Please verify task type and label column name."
    TRANSFORMER_Y_MIN_GREATER = "{transformer_name} error. 'y_min' is greater than the observed minimum in 'y'. " \
                                "Please consider either clipping 'y' to the domain, or pass safe=True during " \
                                "transformer initialization."
    # endregion

    # region SystemErrorStrings
    AUTOML_INTERNAL = "Encountered an internal AutoML error. Error Message/Code: {error_details}"
    DATA = "Encountered an error while reading or writing the Dataset. Error Message/Code: {error_details}"
    SERVICE = "Encountered an error while communicating with the service. Error Message/Code: {error_details}"
    # endregion
