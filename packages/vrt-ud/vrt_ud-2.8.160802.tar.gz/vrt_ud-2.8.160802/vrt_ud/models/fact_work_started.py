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


class FactWorkStarted(object):
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
        'performer_id': 'str',
        'trip_id': 'str',
        'order_id': 'str',
        'demand_key': 'str',
        'fact_time': 'datetime'
    }

    attribute_map = {
        'performer_id': 'performer_id',
        'trip_id': 'trip_id',
        'order_id': 'order_id',
        'demand_key': 'demand_key',
        'fact_time': 'fact_time'
    }

    def __init__(self, performer_id=None, trip_id=None, order_id=None, demand_key=None, fact_time=None, local_vars_configuration=None):  # noqa: E501
        """FactWorkStarted - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._performer_id = None
        self._trip_id = None
        self._order_id = None
        self._demand_key = None
        self._fact_time = None
        self.discriminator = None

        self.performer_id = performer_id
        self.trip_id = trip_id
        self.order_id = order_id
        self.demand_key = demand_key
        if fact_time is not None:
            self.fact_time = fact_time

    @property
    def performer_id(self):
        """Gets the performer_id of this FactWorkStarted.  # noqa: E501

        Performer's ID.  # noqa: E501

        :return: The performer_id of this FactWorkStarted.  # noqa: E501
        :rtype: str
        """
        return self._performer_id

    @performer_id.setter
    def performer_id(self, performer_id):
        """Sets the performer_id of this FactWorkStarted.

        Performer's ID.  # noqa: E501

        :param performer_id: The performer_id of this FactWorkStarted.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and performer_id is None:  # noqa: E501
            raise ValueError("Invalid value for `performer_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                performer_id is not None and len(performer_id) > 1024):
            raise ValueError("Invalid value for `performer_id`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                performer_id is not None and len(performer_id) < 1):
            raise ValueError("Invalid value for `performer_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._performer_id = performer_id

    @property
    def trip_id(self):
        """Gets the trip_id of this FactWorkStarted.  # noqa: E501

        Trip ID.  # noqa: E501

        :return: The trip_id of this FactWorkStarted.  # noqa: E501
        :rtype: str
        """
        return self._trip_id

    @trip_id.setter
    def trip_id(self, trip_id):
        """Sets the trip_id of this FactWorkStarted.

        Trip ID.  # noqa: E501

        :param trip_id: The trip_id of this FactWorkStarted.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and trip_id is None:  # noqa: E501
            raise ValueError("Invalid value for `trip_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                trip_id is not None and len(trip_id) > 1024):
            raise ValueError("Invalid value for `trip_id`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                trip_id is not None and len(trip_id) < 1):
            raise ValueError("Invalid value for `trip_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._trip_id = trip_id

    @property
    def order_id(self):
        """Gets the order_id of this FactWorkStarted.  # noqa: E501

        Order ID.  # noqa: E501

        :return: The order_id of this FactWorkStarted.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this FactWorkStarted.

        Order ID.  # noqa: E501

        :param order_id: The order_id of this FactWorkStarted.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and order_id is None:  # noqa: E501
            raise ValueError("Invalid value for `order_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                order_id is not None and len(order_id) > 1024):
            raise ValueError("Invalid value for `order_id`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                order_id is not None and len(order_id) < 1):
            raise ValueError("Invalid value for `order_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._order_id = order_id

    @property
    def demand_key(self):
        """Gets the demand_key of this FactWorkStarted.  # noqa: E501

        Demand key.  # noqa: E501

        :return: The demand_key of this FactWorkStarted.  # noqa: E501
        :rtype: str
        """
        return self._demand_key

    @demand_key.setter
    def demand_key(self, demand_key):
        """Sets the demand_key of this FactWorkStarted.

        Demand key.  # noqa: E501

        :param demand_key: The demand_key of this FactWorkStarted.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and demand_key is None:  # noqa: E501
            raise ValueError("Invalid value for `demand_key`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                demand_key is not None and len(demand_key) > 1024):
            raise ValueError("Invalid value for `demand_key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                demand_key is not None and len(demand_key) < 1):
            raise ValueError("Invalid value for `demand_key`, length must be greater than or equal to `1`")  # noqa: E501

        self._demand_key = demand_key

    @property
    def fact_time(self):
        """Gets the fact_time of this FactWorkStarted.  # noqa: E501

        Fact time in the [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :return: The fact_time of this FactWorkStarted.  # noqa: E501
        :rtype: datetime
        """
        return self._fact_time

    @fact_time.setter
    def fact_time(self, fact_time):
        """Sets the fact_time of this FactWorkStarted.

        Fact time in the [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :param fact_time: The fact_time of this FactWorkStarted.  # noqa: E501
        :type: datetime
        """

        self._fact_time = fact_time

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
        if not isinstance(other, FactWorkStarted):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FactWorkStarted):
            return True

        return self.to_dict() != other.to_dict()
