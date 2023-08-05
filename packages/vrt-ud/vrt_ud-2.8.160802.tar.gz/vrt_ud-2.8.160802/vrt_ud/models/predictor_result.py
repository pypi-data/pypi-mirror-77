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


class PredictorResult(object):
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
        'windows': 'list[PredictResultWindow]'
    }

    attribute_map = {
        'windows': 'windows'
    }

    def __init__(self, windows=None, local_vars_configuration=None):  # noqa: E501
        """PredictorResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._windows = None
        self.discriminator = None

        if windows is not None:
            self.windows = windows

    @property
    def windows(self):
        """Gets the windows of this PredictorResult.  # noqa: E501

        List of possible windows to fulfil an order.  # noqa: E501

        :return: The windows of this PredictorResult.  # noqa: E501
        :rtype: list[PredictResultWindow]
        """
        return self._windows

    @windows.setter
    def windows(self, windows):
        """Sets the windows of this PredictorResult.

        List of possible windows to fulfil an order.  # noqa: E501

        :param windows: The windows of this PredictorResult.  # noqa: E501
        :type: list[PredictResultWindow]
        """

        self._windows = windows

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
        if not isinstance(other, PredictorResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PredictorResult):
            return True

        return self.to_dict() != other.to_dict()
