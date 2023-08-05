# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for all the forecasting related parameters."""
from typing import Any, Dict, List, Optional, Union
import logging

from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentBlankOrEmpty, ArgumentOutOfRange
from azureml.automl.core.shared._diagnostics.automl_error_definitions import InvalidArgumentType, \
    InvalidArgumentWithSupportedValues, TimeseriesInvalidDateOffsetType
from azureml.automl.core.shared.constants import (TimeSeries,
                                                  TimeSeriesInternal,
                                                  TimeSeriesWebLinks)
from azureml.automl.core.shared.exceptions import ConfigException
from azureml.automl.core.shared.reference_codes import ReferenceCodes


logger = logging.getLogger(__name__)


class ForecastingParameters:
    DEPRECATED_DICT = {
        TimeSeries.MAX_HORIZON: TimeSeries.FORECAST_HORIZON,
        TimeSeries.GRAIN_COLUMN_NAMES: TimeSeries.TIME_SERIES_ID_COLUMN_NAMES,
        TimeSeries.COUNTRY_OR_REGION: TimeSeries.COUNTRY_OR_REGION_FOR_HOLIDAYS,
        TimeSeries.COUNTRY: TimeSeries.COUNTRY_OR_REGION_FOR_HOLIDAYS,
        TimeSeries.HOLIDAY_COUNTRY: TimeSeries.COUNTRY_OR_REGION_FOR_HOLIDAYS
    }

    DEFAULT_TIMESERIES_VALUE = {
        TimeSeries.FORECAST_HORIZON: TimeSeriesInternal.MAX_HORIZON_DEFAULT,
        TimeSeries.MAX_HORIZON: TimeSeriesInternal.MAX_HORIZON_DEFAULT,
        TimeSeries.TARGET_ROLLING_WINDOW_SIZE: TimeSeriesInternal.WINDOW_SIZE_DEFDAULT,
        TimeSeries.TARGET_LAGS: TimeSeriesInternal.TARGET_LAGS_DEFAULT,
        TimeSeries.FEATURE_LAGS: TimeSeriesInternal.FEATURE_LAGS_DEFAULT,
        TimeSeries.SEASONALITY: TimeSeriesInternal.SEASONALITY_VALUE_DEFAULT,
        TimeSeries.SHORT_SERIES_HANDLING: TimeSeriesInternal.SHORT_SERIES_HANDLING_DEFAULT,
        TimeSeries.USE_STL: TimeSeriesInternal.USE_STL_DEFAULT,
        TimeSeries.FREQUENCY: TimeSeriesInternal.FREQUENCY_DEFAULT
    }

    MAX_LAG_LENGTH = 2000

    def __init__(
            self,
            time_column_name: Optional[str] = None,
            forecast_horizon: Optional[Union[str, int]] = TimeSeriesInternal.MAX_HORIZON_DEFAULT,
            time_series_id_column_names: Optional[Union[str, List[str]]] = None,
            drop_column_names: Optional[Union[str, List[str]]] = None,
            group_column_names: Optional[Union[str, List[str]]] = None,
            target_lags: Optional[Union[List[int], int, str]] = TimeSeriesInternal.TARGET_LAGS_DEFAULT,
            feature_lags: Optional[str] = TimeSeriesInternal.FEATURE_LAGS_DEFAULT,
            target_rolling_window_size: Optional[Union[str, int]] = TimeSeriesInternal.WINDOW_SIZE_DEFDAULT,
            holiday_country: Optional[str] = None,
            seasonality: Optional[Union[str, int]] = TimeSeriesInternal.SEASONALITY_VALUE_DEFAULT,
            country_or_region_for_holidays: Optional[str] = None,
            use_stl: Optional[str] = TimeSeriesInternal.USE_STL_DEFAULT,
            short_series_handling: bool = TimeSeriesInternal.SHORT_SERIES_HANDLING_DEFAULT,
            freq: Optional[str] = None,
            validate_parameters: Optional[bool] = True
    ):
        """
        Manage parameters used by forecasting tasks.

        :param time_column_name:
            The name of the time column. This parameter is required when forecasting to specify the datetime
            column in the input data used for building the time series and inferring its frequency.
        :type time_column_name: str
        :param forecast_horizon:
            The desired maximum forecast horizon in units of time-series frequency. The default value is 1.

            Units are based on the time interval of your training data, e.g., monthly, weekly that the forecaster
            should predict out. When task type is forecasting, this parameter is required. For more information on
            setting forecasting parameters, see `Auto-train a time-series forecast model <https://docs.microsoft.com/
            azure/machine-learning/how-to-auto-train-forecast>`_.
        :type forecast_horizon: int
        :param time_series_id_column_names:
            The names of columns used to group a timeseries.
            It can be used to create multiple series. If grain is not defined, the data set is assumed
            to be one time-series. This parameter is used with task type forecasting.
        :type time_series_id_column_names: str or list(str)
        :param drop_column_names:
            The names of columns to drop for forecasting tasks. To customize drop columns for classification
            and regression tasks, use the ``featurization`` parameter.
        :type drop_column_names: str or list(str)
        :param target_lags:
            The number of past periods to lag from the target column. The default is 1.

            When forecasting, this parameter represents the number of rows to lag the target values based
            on the frequency of the data. This is represented as a list or single integer. Lag should be used
            when the relationship between the independent variables and dependant variable do not match up or
            correlate by default. For example, when trying to forecast demand for a product, the demand in any
            month may depend on the price of specific commodities 3 months prior. In this example, you may want
            to lag the target (demand) negatively by 3 months so that the model is training on the correct
            relationship. For more information, see `Auto-train a time-series forecast model
            <https://docs.microsoft.com/azure/machine-learning/how-to-auto-train-forecast>`_.
        :type target_lags: int or list(int)
        :param feature_lags: Flag for generating lags for the numeric features with 'auto' or None.
        :type feature_lags: str or None
        :param target_rolling_window_size:
            The number of past periods used to create a rolling window average of the target column.

            When forecasting, this parameter represents `n` historical periods to use to generate forecasted values,
            <= training set size. If omitted, `n` is the full training set size. Specify this parameter
            when you only want to consider a certain amount of history when training the model.
        :type target_rolling_window_size: int
        :param holiday_country: The country/region used to generate holiday features.
            These should be ISO 3166 two-letter country/region codes, for example 'US' or 'GB'.
        :type country_or_region_for_holidays: str
        :param country_or_region_for_holidays: The country/region used to generate holiday features.
            These should be ISO 3166 two-letter country/region codes, for example 'US' or 'GB'.
        :type country_or_region_for_holidays: str
        :param use_stl: Configure STL Decomposition of the time-series target column.
                    use_stl can take three values: None (default) - no stl decomposition, 'season' - only generate
                    season component and season_trend - generate both season and trend components.
        :type use_stl: str
        :param seasonality: Set time series seasonality. If seasonality is set to -1, it will be inferred.
                    If use_stl is not set, this parameter will not be used.
        :type seasonality: int
        :param short_series_handling: Configure short series handling for forecasting tasks.
        :type short_series_handling: bool
        :param validate_parameters: Configure to validate input parameters.
        :type validate_parameters: bool
        """
        self._time_column_name = time_column_name
        self._forecast_horizon = forecast_horizon
        self._time_series_id_column_names = time_series_id_column_names
        self._target_lags = target_lags
        self._feature_lags = feature_lags
        self._target_rolling_window_size = target_rolling_window_size
        self._group_column_names = group_column_names
        self._drop_column_names = drop_column_names
        self._seasonality = seasonality
        self._use_stl = use_stl
        self._short_series_handling = short_series_handling
        self._freq = freq  # type: Optional[str]

        self._country_or_region_for_holidays = None
        if country_or_region_for_holidays is not None:
            self._country_or_region_for_holidays = country_or_region_for_holidays
            if holiday_country is not None:
                self._print_deprecated_neglected_message(
                    TimeSeries.HOLIDAY_COUNTRY, TimeSeries.COUNTRY_OR_REGION_FOR_HOLIDAYS)
        elif holiday_country is not None:
            self._country_or_region_for_holidays = holiday_country
            self._print_deprecated_message(TimeSeries.HOLIDAY_COUNTRY, TimeSeries.COUNTRY_OR_REGION_FOR_HOLIDAYS)

        self._formatted_target_lags = None   # type: Optional[Dict[str, List[Union[int, str]]]]
        self._formatted_id_column_names = None  # type: Optional[List[str]]
        self._formatted_drop_column_names = None  # type: Optional[List[str]]
        self._formatted_group_column_names = None  # type: Optional[List[str]]

        if validate_parameters:
            self.validate_parameters()

    def validate_parameters(self):
        """
        Validate the parameters in the ForecastingParameters class.
        """
        self._validate_time_column_name()
        self._validate_time_series_id_column_names()
        self._validate_forecast_horizon()
        self._validate_target_rolling_window_size()
        self._validate_target_lags()
        self._validate_feature_lags()
        self._validate_freq(self._freq)

    @property
    def forecast_horizon(self) -> Union[str, int, None]:
        """
        The desired maximum forecast horizon in units of time-series frequency. The default value is 1.
        Units are based on the time interval of your training data,
        e.g., monthly, weekly that the forecaster should predict out.
        """
        return self._forecast_horizon

    @forecast_horizon.setter
    def forecast_horizon(self, forecast_horizon: Optional[Union[str, int, None]]) -> None:
        self._forecast_horizon = forecast_horizon
        self._validate_forecast_horizon()

    @property
    def formatted_time_series_id_column_names(self) -> Optional[List[str]]:
        """
        The names of columns used to group a timeseries. It can be used to create multiple series.
        If time_series_id_column_names is not defined, the data set is assumed to be one time-series.
        """
        if self._formatted_id_column_names is not None:
            return self._formatted_id_column_names

        self._formatted_id_column_names = self._make_column_names_list(
            self.time_series_id_column_names, use_empty_list=False)
        return self._formatted_id_column_names

    @property
    def time_series_id_column_names(self) -> Union[str, List[str], None]:
        """
        The names of columns used to group a timeseries. It can be used to create multiple series.
        If time_series_id_column_names is not defined, the data set is assumed to be one time-series.
        """
        return self._time_series_id_column_names

    @time_series_id_column_names.setter
    def time_series_id_column_names(self, time_series_id_column_names: Union[str, List[str], None]) -> None:
        self._time_series_id_column_names = time_series_id_column_names
        self._formatted_id_column_names = None
        self._validate_time_series_id_column_names()

    @property
    def time_column_name(self) -> Optional[str]:
        """
        The name of the time column. This parameter is required when forecasting to specify the datetime
        column in the input data used for building the time series and inferring its frequency.
        """
        return self._time_column_name

    @time_column_name.setter
    def time_column_name(self, time_column_name: Optional[str]) -> None:
        self._time_column_name = time_column_name
        self._validate_time_column_name()

    @property
    def formatted_target_lags(self) -> Optional[Dict[str, List[Union[int, str]]]]:
        """
        The formatted number of past periods to lag from the target column.
        """
        if self._formatted_target_lags is not None:
            return self._formatted_target_lags

        target_lags = None  # type: Optional[List[Union[int, str]]]

        if isinstance(self._target_lags, int) or isinstance(self._target_lags, list):
            if isinstance(self._target_lags, int):
                target_lags = [self._target_lags]
            else:
                # Get unique values and preserve order for unittests.
                target_lags = sorted(set(self._target_lags))
            if len(target_lags) == 0:
                target_lags = None
        elif self._target_lags == TimeSeries.AUTO:
            target_lags = [TimeSeries.AUTO]
        elif self._target_lags is None:
            target_lags = None

        # Convert target lags to dictionary or None.
        if target_lags is not None:
            lags = {TimeSeriesInternal.DUMMY_TARGET_COLUMN:
                    target_lags}  # type: Optional[Dict[str, List[Union[int, str]]]]
        else:
            lags = None

        self._formatted_target_lags = lags

        return lags

    @property
    def target_lags(self) -> Union[List[int], int, str, None]:
        """
        The number of past periods to lag from the target column.
        """
        return self._target_lags

    @target_lags.setter
    def target_lags(self, target_lags: Union[List[int], int, str, None]) -> None:
        self._target_lags = target_lags
        self._formatted_target_lags = None
        self._validate_target_lags()

    @property
    def target_rolling_window_size(self) -> Optional[Union[str, int]]:
        return self._target_rolling_window_size

    @target_rolling_window_size.setter
    def target_rolling_window_size(self, target_rolling_window_size: Optional[Union[str, int]]) -> None:
        """The number of past periods used to create a rolling window average of the target column."""
        self._target_rolling_window_size = target_rolling_window_size
        self._validate_target_rolling_window_size()

    @property
    def holiday_country(self) -> Optional[str]:
        """
        The country/region used to generate holiday features.
        These should be ISO 3166 two-letter country/region code, for example 'US' or 'GB'.
        """
        self._print_deprecated_message(TimeSeries.HOLIDAY_COUNTRY, TimeSeries.COUNTRY_OR_REGION_FOR_HOLIDAYS)
        return self._country_or_region_for_holidays

    @property
    def country_or_region_for_holidays(self) -> Optional[str]:
        """
        The country/region used to generate holiday features.
        These should be ISO 3166 two-letter country/region code, for example 'US' or 'GB'.
        """
        return self._country_or_region_for_holidays

    @country_or_region_for_holidays.setter
    def country_or_region_for_holidays(self, country_or_region_for_holidays: Optional[str]) -> None:
        self._country_or_region_for_holidays = country_or_region_for_holidays

    @property
    def feature_lags(self) -> Optional[str]:
        """Flag for generating lags for the numeric features."""
        return self._feature_lags

    @feature_lags.setter
    def feature_lags(self, feature_lags: Optional[str]) -> None:
        self._feature_lags = feature_lags
        self._validate_feature_lags()

    @property
    def use_stl(self) -> Optional[str]:
        """
        Configure STL Decomposition of the time-series target column.
        use_stl can take three values: None (default) - no stl decomposition,
        'season' - only generate season component and season_trend - generate both season and trend components.
        """
        return self._use_stl

    @use_stl.setter
    def use_stl(self, use_stl: Optional[str]) -> None:
        self._use_stl = use_stl

    @property
    def formatted_drop_column_names(self) -> Optional[List[str]]:
        """
        The formatted names of columns to drop for forecasting tasks.
        """
        if self._formatted_drop_column_names is not None:
            return self._formatted_drop_column_names

        self._formatted_drop_column_names = self._make_column_names_list(
            self._drop_column_names, use_empty_list=True)
        return self._formatted_drop_column_names

    @property
    def drop_column_names(self) -> Optional[Union[str, List[str]]]:
        """
        The names of columns to drop for forecasting tasks.
        """
        return self._drop_column_names

    @drop_column_names.setter
    def drop_column_names(self, drop_column_names: Optional[Union[str, List[str]]]) -> None:
        self._drop_column_names = drop_column_names
        self._formatted_drop_column_names = None

    @property
    def formatted_group_column_names(self) -> Optional[List[str]]:
        if self._formatted_group_column_names is not None:
            return self._formatted_group_column_names

        self._formatted_group_column_names = self._make_column_names_list(
            self._group_column_names, use_empty_list=False)

        return self._formatted_group_column_names

    @property
    def group_column_names(self) -> Optional[Union[str, List[str]]]:
        return self._group_column_names

    @group_column_names.setter
    def group_column_names(self, group_column_names: Optional[Union[str, List[str]]]) -> None:
        self._group_column_names = group_column_names
        self._formatted_group_column_names = None

    @property
    def seasonality(self) -> Optional[Union[str, int]]:
        """
        Set time series seasonality. If seasonality is set to 'auto', it will be inferred.
        If use_stl is not set, this parameter will not be used.
        """
        return self._seasonality

    @seasonality.setter
    def seasonality(self, seasonality: Optional[Union[str, int]]) -> None:
        self._seasonality = seasonality

    @property
    def short_series_handling(self) -> bool:
        """
        Configure short series handling for forecasting tasks.
        """
        return self._short_series_handling

    @short_series_handling.setter
    def short_series_handling(self, short_series_handling: bool) -> None:
        self._short_series_handling = short_series_handling

    @property
    def dropna(self) -> bool:
        """Configure dropna in timeseries data transformer."""
        return TimeSeriesInternal.DROP_NA_DEFAULT

    @property
    def overwrite_columns(self) -> bool:
        """Configure overwrite_columns in timeseries data transformer."""
        return TimeSeriesInternal.OVERWRITE_COLUMNS_DEFAULT

    @property
    def transform_dictionary(self) -> Dict[str, Any]:
        """Configure transform_dictionary in timeseries data transformer."""
        return TimeSeriesInternal.TRANSFORM_DICT_DEFAULT

    @staticmethod
    def from_parameters_dict(
            parameter_dict: Dict[str, Any],
            validate_params: bool,
            show_deprecate_warnings: Optional[bool] = True
    ) -> 'ForecastingParameters':
        """
        Construct ForecastingParameters class from a dict.

        :param parameter_dict: The dict contains all the forecasting parameters.
        :param validate_params: Whether validate input parameter or not.
        :param show_deprecate_warnings: Switch to show deprecated parameters warning.
        """
        # We will validate the parameters after we will set it.
        forecasting_params = ForecastingParameters(validate_parameters=False)
        for param in TimeSeries.ALL_FORECASTING_PARAMETERS:
            default_value = ForecastingParameters.DEFAULT_TIMESERIES_VALUE.get(param)
            if param in parameter_dict:
                # if any parameter found in deprecated dict, the corresponding new one needs set to be none to bypass
                # the updated one when retrieving that one.
                if param in ForecastingParameters.DEPRECATED_DICT.keys():
                    new_param = ForecastingParameters.DEPRECATED_DICT[param]
                    if new_param in parameter_dict and show_deprecate_warnings:
                        forecasting_params._print_deprecated_neglected_message(param, new_param)
                    else:
                        if show_deprecate_warnings:
                            forecasting_params._print_deprecated_message(param, new_param)
                        setattr(
                            forecasting_params,
                            forecasting_params._get_attribute_name(new_param),
                            parameter_dict.get(param, default_value)
                        )
                else:
                    setattr(
                        forecasting_params,
                        forecasting_params._get_attribute_name(param),
                        parameter_dict.get(param, default_value))

        if validate_params:
            forecasting_params.validate_parameters()

        return forecasting_params

    @property
    def freq(self) -> Optional[str]:
        """The frequencu of the data set."""
        return self._freq

    @freq.setter
    def freq(self, val: Optional[str]) -> None:
        """Set the data set frequency"""
        self._validate_freq(val)
        self._freq = val

    def _validate_time_column_name(self) -> None:
        if self.time_column_name is None:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentBlankOrEmpty, target="time_column_name", argument_name="time_column_name",
                    reference_code=ReferenceCodes._FORECASTING_PARAM_TIME_COLUMN_MISSING
                )
            )

    def _validate_time_series_id_column_names(self) -> None:
        id_column_names = self._time_series_id_column_names
        expected_types = ', '.join(["str", "List[str]", "None"])
        if isinstance(id_column_names, list):
            for col in id_column_names:
                self._check_column_name_type(
                    col, TimeSeries.TIME_SERIES_ID_COLUMN_NAMES,
                    expected_types,
                    ReferenceCodes._FORECASTING_PARAM_ID_COL_NAMES_LIST_INVALID_TYPE)
        elif id_column_names is not None:
            self._check_column_name_type(
                id_column_names, TimeSeries.TIME_SERIES_ID_COLUMN_NAMES,
                expected_types,
                ReferenceCodes._FORECASTING_PARAM_ID_COL_NAMES_INVALID_TYPE)

    def _check_column_name_type(
            self, col_name: Any,
            target: str,
            expected_values: str,
            reference_code: str
    ) -> None:
        if not isinstance(col_name, str):
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType, actual_type=type(col_name),
                    expected_types=expected_values,
                    target=target, argument="time_series_id_column_names ({})".format(str(col_name)),
                    reference_code=reference_code)
            )

    def _validate_target_rolling_window_size(self):
        ForecastingParameters._is_int_or_auto(
            self.target_rolling_window_size, TimeSeries.TARGET_ROLLING_WINDOW_SIZE,
            ReferenceCodes._FORECASTING_PARAM_TARGET_ROLLING_WINDOW_SIZE_INVALID_TYPE)

        if isinstance(self.target_rolling_window_size, int) and self.target_rolling_window_size < 2:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentOutOfRange, target=TimeSeries.TARGET_ROLLING_WINDOW_SIZE,
                    argument_name=TimeSeries.TARGET_ROLLING_WINDOW_SIZE, min=2, max="inf",
                    reference_code=ReferenceCodes._TARGET_ROLLING_WINDOW_SMALL
                )
            )

    def _validate_target_lags(self) -> None:
        if self._target_lags is None or self._target_lags == TimeSeries.AUTO:
            return
        elif isinstance(self._target_lags, int):
            self._check_target_lags_range(self._target_lags)
        elif isinstance(self._target_lags, list):
            for lag in self._target_lags:
                if not isinstance(lag, int):
                    raise ConfigException._with_error(
                        AzureMLError.create(
                            InvalidArgumentType, target="target_lags", argument="target_lags ({})".format(lag),
                            actual_type=type(lag), expected_types="int",
                            reference_code=ReferenceCodes._FORECASTING_PARAM_TARGET_LAG_LIST_INVALID_TYPE)
                    )
                else:
                    self._check_target_lags_range(lag)
        else:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType, target="target_lags", argument="target_lags ({})".format(self._target_lags),
                    actual_type=type(self._target_lags), expected_types=", ".join(
                        ["int", "List[int]", TimeSeries.AUTO]),
                    reference_code=ReferenceCodes._FORECASTING_PARAM_TARGET_LAG_NOT_SUPPORTED)
            )

    def _check_target_lags_range(self, lag: int) -> None:
        if lag < 1 or lag > ForecastingParameters.MAX_LAG_LENGTH:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentOutOfRange, target=TimeSeries.TARGET_LAGS,
                    argument_name="{} ({})".format(TimeSeries.TARGET_LAGS, lag),
                    min=1, max=ForecastingParameters.MAX_LAG_LENGTH,
                    reference_code=ReferenceCodes._FORECASTING_PARAM_TARGET_LAG_OUT_OF_RANGE
                )
            )

    def _validate_feature_lags(self) -> None:
        permitted_feature_lags_options = [TimeSeries.AUTO, TimeSeriesInternal.FEATURE_LAGS_DEFAULT]
        if self.feature_lags not in permitted_feature_lags_options:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues, target=TimeSeries.FEATURE_LAGS,
                    arguments="{} ({})".format(TimeSeries.FEATURE_LAGS, self.feature_lags),
                    supported_values=", ".join([str(k) for k in permitted_feature_lags_options]),
                    reference_code=ReferenceCodes._FORECASTING_PARAM_FEATURE_LAGS_INVALID_TYPE
                )
            )

    def _validate_forecast_horizon(self) -> None:
        ForecastingParameters._is_int_or_auto(
            self.forecast_horizon, TimeSeries.FORECAST_HORIZON,
            ReferenceCodes._FORECASTING_PARAM_HORIZON_INVALID_TYPE, False)

    def _validate_freq(self, val: Any) -> None:
        """Validate the data set frequency parameter."""
        if val is not None and not isinstance(val, str):
            raise ConfigException._with_error(
                AzureMLError.create(
                    TimeseriesInvalidDateOffsetType, target="freq", pandas_url=TimeSeriesWebLinks.PANDAS_DO_URL,
                    reference_code=ReferenceCodes._FORECASTING_PARAM_FREQ_TYPE)
            )

    def _print_deprecated_message(self, old_parameter_name, new_parameter_name):
        msg = "Forecasting parameter {} will be deprecated in the future, " \
              "please use {} instead.".format(old_parameter_name, new_parameter_name)
        logging.warning(msg)
        logger.warning(msg)

    def _print_deprecated_neglected_message(self, old_parameter_name, new_parameter_name):
        msg = "Both forecasting parameter {} and {} are found from input. " \
              "The deprecated one {} " \
              "will be neglected.".format(old_parameter_name, new_parameter_name, old_parameter_name)
        logging.warning(msg)
        logger.warning(msg)

    def _set_default_value(self) -> None:
        for param, default_value in self.DEFAULT_TIMESERIES_VALUE:
            if getattr(self, self._get_attribute_name(param), None) is None:
                setattr(self, self._get_attribute_name(param), default_value)

    def _get_attribute_name(self, forecasting_parameter_name: str) -> str:
        return "_" + forecasting_parameter_name

    def _make_column_names_list(
            self,
            column_names: Union[str, List[str], None],
            use_empty_list: Optional[bool] = False
    ) -> Optional[List[str]]:
        if column_names is None:
            return None if not use_empty_list else list()
        elif isinstance(column_names, list):
            if len(column_names) == 0 and not use_empty_list:
                return None
            return column_names
        else:
            return [column_names]

    @staticmethod
    def _is_int_or_auto(val: Optional[Any], val_name: str, reference_code: str, allow_none: bool = True) -> None:
        """
        Raise a ConfigException if value is not 'auto' or integer.

        :param val: The value to test.
        :param val_name: the name of a value to be displayed in the error message.
        :param allow_none: if true, the None value is allowed for val.
        :raises: ConfigException
        """
        if allow_none and val is None:
            return
        if not isinstance(val, int) and val != TimeSeries.AUTO:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentType, target=val_name, reference_code=reference_code,
                    argument="{} ({})".format(val_name, val), actual_type=type(val),
                    expected_types=", ".join(['int', TimeSeries.AUTO]))
            )
