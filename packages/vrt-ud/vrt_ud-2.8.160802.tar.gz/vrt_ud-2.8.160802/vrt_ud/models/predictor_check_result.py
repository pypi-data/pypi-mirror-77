# coding: utf-8

"""
    VeeRoute.UD

    VeeRoute.UD API  # noqa: E501

    The version of the OpenAPI document: 2.8.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from vrt_ud.configuration import Configuration


class PredictorCheckResult(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'currently_started_data_preparation': 'datetime',
        'previous_data_preparation': 'datetime',
        'last_succesful_data_preparation': 'datetime',
        'validation_result': 'str',
        'current_data_preparation_errors': 'str',
        'last_owp_validation_errors': 'str'
    }

    attribute_map = {
        'currently_started_data_preparation': 'currently_started_data_preparation',
        'previous_data_preparation': 'previous_data_preparation',
        'last_succesful_data_preparation': 'last_succesful_data_preparation',
        'validation_result': 'validation_result',
        'current_data_preparation_errors': 'current_data_preparation_errors',
        'last_owp_validation_errors': 'last_owp_validation_errors'
    }

    def __init__(self, currently_started_data_preparation=None, previous_data_preparation=None, last_succesful_data_preparation=None, validation_result=None, current_data_preparation_errors=None, last_owp_validation_errors=None, local_vars_configuration=None):  # noqa: E501
        """PredictorCheckResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._currently_started_data_preparation = None
        self._previous_data_preparation = None
        self._last_succesful_data_preparation = None
        self._validation_result = None
        self._current_data_preparation_errors = None
        self._last_owp_validation_errors = None
        self.discriminator = None

        if currently_started_data_preparation is not None:
            self.currently_started_data_preparation = currently_started_data_preparation
        if previous_data_preparation is not None:
            self.previous_data_preparation = previous_data_preparation
        if last_succesful_data_preparation is not None:
            self.last_succesful_data_preparation = last_succesful_data_preparation
        if validation_result is not None:
            self.validation_result = validation_result
        if current_data_preparation_errors is not None:
            self.current_data_preparation_errors = current_data_preparation_errors
        if last_owp_validation_errors is not None:
            self.last_owp_validation_errors = last_owp_validation_errors

    @property
    def currently_started_data_preparation(self):
        """Gets the currently_started_data_preparation of this PredictorCheckResult.  # noqa: E501

        Time of the last scenario start.  # noqa: E501

        :return: The currently_started_data_preparation of this PredictorCheckResult.  # noqa: E501
        :rtype: datetime
        """
        return self._currently_started_data_preparation

    @currently_started_data_preparation.setter
    def currently_started_data_preparation(self, currently_started_data_preparation):
        """Sets the currently_started_data_preparation of this PredictorCheckResult.

        Time of the last scenario start.  # noqa: E501

        :param currently_started_data_preparation: The currently_started_data_preparation of this PredictorCheckResult.  # noqa: E501
        :type: datetime
        """

        self._currently_started_data_preparation = currently_started_data_preparation

    @property
    def previous_data_preparation(self):
        """Gets the previous_data_preparation of this PredictorCheckResult.  # noqa: E501

        Time of the previous scenario start.  # noqa: E501

        :return: The previous_data_preparation of this PredictorCheckResult.  # noqa: E501
        :rtype: datetime
        """
        return self._previous_data_preparation

    @previous_data_preparation.setter
    def previous_data_preparation(self, previous_data_preparation):
        """Sets the previous_data_preparation of this PredictorCheckResult.

        Time of the previous scenario start.  # noqa: E501

        :param previous_data_preparation: The previous_data_preparation of this PredictorCheckResult.  # noqa: E501
        :type: datetime
        """

        self._previous_data_preparation = previous_data_preparation

    @property
    def last_succesful_data_preparation(self):
        """Gets the last_succesful_data_preparation of this PredictorCheckResult.  # noqa: E501

        Time of the last successful scenario playback.  # noqa: E501

        :return: The last_succesful_data_preparation of this PredictorCheckResult.  # noqa: E501
        :rtype: datetime
        """
        return self._last_succesful_data_preparation

    @last_succesful_data_preparation.setter
    def last_succesful_data_preparation(self, last_succesful_data_preparation):
        """Sets the last_succesful_data_preparation of this PredictorCheckResult.

        Time of the last successful scenario playback.  # noqa: E501

        :param last_succesful_data_preparation: The last_succesful_data_preparation of this PredictorCheckResult.  # noqa: E501
        :type: datetime
        """

        self._last_succesful_data_preparation = last_succesful_data_preparation

    @property
    def validation_result(self):
        """Gets the validation_result of this PredictorCheckResult.  # noqa: E501

        Data validation result from the last scenario launching.  # noqa: E501

        :return: The validation_result of this PredictorCheckResult.  # noqa: E501
        :rtype: str
        """
        return self._validation_result

    @validation_result.setter
    def validation_result(self, validation_result):
        """Sets the validation_result of this PredictorCheckResult.

        Data validation result from the last scenario launching.  # noqa: E501

        :param validation_result: The validation_result of this PredictorCheckResult.  # noqa: E501
        :type: str
        """

        self._validation_result = validation_result

    @property
    def current_data_preparation_errors(self):
        """Gets the current_data_preparation_errors of this PredictorCheckResult.  # noqa: E501

        Errors in the last scenario launching.  # noqa: E501

        :return: The current_data_preparation_errors of this PredictorCheckResult.  # noqa: E501
        :rtype: str
        """
        return self._current_data_preparation_errors

    @current_data_preparation_errors.setter
    def current_data_preparation_errors(self, current_data_preparation_errors):
        """Sets the current_data_preparation_errors of this PredictorCheckResult.

        Errors in the last scenario launching.  # noqa: E501

        :param current_data_preparation_errors: The current_data_preparation_errors of this PredictorCheckResult.  # noqa: E501
        :type: str
        """

        self._current_data_preparation_errors = current_data_preparation_errors

    @property
    def last_owp_validation_errors(self):
        """Gets the last_owp_validation_errors of this PredictorCheckResult.  # noqa: E501

        Errors in the previous scenario launching.  # noqa: E501

        :return: The last_owp_validation_errors of this PredictorCheckResult.  # noqa: E501
        :rtype: str
        """
        return self._last_owp_validation_errors

    @last_owp_validation_errors.setter
    def last_owp_validation_errors(self, last_owp_validation_errors):
        """Sets the last_owp_validation_errors of this PredictorCheckResult.

        Errors in the previous scenario launching.  # noqa: E501

        :param last_owp_validation_errors: The last_owp_validation_errors of this PredictorCheckResult.  # noqa: E501
        :type: str
        """

        self._last_owp_validation_errors = last_owp_validation_errors

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PredictorCheckResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PredictorCheckResult):
            return True

        return self.to_dict() != other.to_dict()
