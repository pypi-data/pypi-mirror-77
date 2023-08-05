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


class FactEventWindowChanged(object):
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
        'location_id': 'str',
        'old_hard_time_from': 'datetime',
        'old_hard_time_to': 'datetime',
        'old_soft_time_from': 'datetime',
        'old_soft_time_to': 'datetime',
        'new_hard_time_from': 'datetime',
        'new_hard_time_to': 'datetime',
        'new_soft_time_from': 'datetime',
        'new_soft_time_to': 'datetime',
        'window_change_reason': 'str',
        'fact_time': 'datetime'
    }

    attribute_map = {
        'performer_id': 'performer_id',
        'trip_id': 'trip_id',
        'order_id': 'order_id',
        'demand_key': 'demand_key',
        'location_id': 'location_id',
        'old_hard_time_from': 'old_hard_time_from',
        'old_hard_time_to': 'old_hard_time_to',
        'old_soft_time_from': 'old_soft_time_from',
        'old_soft_time_to': 'old_soft_time_to',
        'new_hard_time_from': 'new_hard_time_from',
        'new_hard_time_to': 'new_hard_time_to',
        'new_soft_time_from': 'new_soft_time_from',
        'new_soft_time_to': 'new_soft_time_to',
        'window_change_reason': 'window_change_reason',
        'fact_time': 'fact_time'
    }

    def __init__(self, performer_id=None, trip_id=None, order_id=None, demand_key=None, location_id=None, old_hard_time_from=None, old_hard_time_to=None, old_soft_time_from=None, old_soft_time_to=None, new_hard_time_from=None, new_hard_time_to=None, new_soft_time_from=None, new_soft_time_to=None, window_change_reason=None, fact_time=None, local_vars_configuration=None):  # noqa: E501
        """FactEventWindowChanged - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._performer_id = None
        self._trip_id = None
        self._order_id = None
        self._demand_key = None
        self._location_id = None
        self._old_hard_time_from = None
        self._old_hard_time_to = None
        self._old_soft_time_from = None
        self._old_soft_time_to = None
        self._new_hard_time_from = None
        self._new_hard_time_to = None
        self._new_soft_time_from = None
        self._new_soft_time_to = None
        self._window_change_reason = None
        self._fact_time = None
        self.discriminator = None

        self.performer_id = performer_id
        self.trip_id = trip_id
        self.order_id = order_id
        self.demand_key = demand_key
        self.location_id = location_id
        if old_hard_time_from is not None:
            self.old_hard_time_from = old_hard_time_from
        if old_hard_time_to is not None:
            self.old_hard_time_to = old_hard_time_to
        if old_soft_time_from is not None:
            self.old_soft_time_from = old_soft_time_from
        if old_soft_time_to is not None:
            self.old_soft_time_to = old_soft_time_to
        if new_hard_time_from is not None:
            self.new_hard_time_from = new_hard_time_from
        if new_hard_time_to is not None:
            self.new_hard_time_to = new_hard_time_to
        if new_soft_time_from is not None:
            self.new_soft_time_from = new_soft_time_from
        if new_soft_time_to is not None:
            self.new_soft_time_to = new_soft_time_to
        if window_change_reason is not None:
            self.window_change_reason = window_change_reason
        if fact_time is not None:
            self.fact_time = fact_time

    @property
    def performer_id(self):
        """Gets the performer_id of this FactEventWindowChanged.  # noqa: E501

        Performer's ID.  # noqa: E501

        :return: The performer_id of this FactEventWindowChanged.  # noqa: E501
        :rtype: str
        """
        return self._performer_id

    @performer_id.setter
    def performer_id(self, performer_id):
        """Sets the performer_id of this FactEventWindowChanged.

        Performer's ID.  # noqa: E501

        :param performer_id: The performer_id of this FactEventWindowChanged.  # noqa: E501
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
        """Gets the trip_id of this FactEventWindowChanged.  # noqa: E501

        Trip ID.  # noqa: E501

        :return: The trip_id of this FactEventWindowChanged.  # noqa: E501
        :rtype: str
        """
        return self._trip_id

    @trip_id.setter
    def trip_id(self, trip_id):
        """Sets the trip_id of this FactEventWindowChanged.

        Trip ID.  # noqa: E501

        :param trip_id: The trip_id of this FactEventWindowChanged.  # noqa: E501
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
        """Gets the order_id of this FactEventWindowChanged.  # noqa: E501

        Order ID.  # noqa: E501

        :return: The order_id of this FactEventWindowChanged.  # noqa: E501
        :rtype: str
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this FactEventWindowChanged.

        Order ID.  # noqa: E501

        :param order_id: The order_id of this FactEventWindowChanged.  # noqa: E501
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
        """Gets the demand_key of this FactEventWindowChanged.  # noqa: E501

        Demand key.  # noqa: E501

        :return: The demand_key of this FactEventWindowChanged.  # noqa: E501
        :rtype: str
        """
        return self._demand_key

    @demand_key.setter
    def demand_key(self, demand_key):
        """Sets the demand_key of this FactEventWindowChanged.

        Demand key.  # noqa: E501

        :param demand_key: The demand_key of this FactEventWindowChanged.  # noqa: E501
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
    def location_id(self):
        """Gets the location_id of this FactEventWindowChanged.  # noqa: E501

        Location key.  # noqa: E501

        :return: The location_id of this FactEventWindowChanged.  # noqa: E501
        :rtype: str
        """
        return self._location_id

    @location_id.setter
    def location_id(self, location_id):
        """Sets the location_id of this FactEventWindowChanged.

        Location key.  # noqa: E501

        :param location_id: The location_id of this FactEventWindowChanged.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and location_id is None:  # noqa: E501
            raise ValueError("Invalid value for `location_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                location_id is not None and len(location_id) > 1024):
            raise ValueError("Invalid value for `location_id`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                location_id is not None and len(location_id) < 1):
            raise ValueError("Invalid value for `location_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._location_id = location_id

    @property
    def old_hard_time_from(self):
        """Gets the old_hard_time_from of this FactEventWindowChanged.  # noqa: E501

        Previous start of the window.  # noqa: E501

        :return: The old_hard_time_from of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._old_hard_time_from

    @old_hard_time_from.setter
    def old_hard_time_from(self, old_hard_time_from):
        """Sets the old_hard_time_from of this FactEventWindowChanged.

        Previous start of the window.  # noqa: E501

        :param old_hard_time_from: The old_hard_time_from of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._old_hard_time_from = old_hard_time_from

    @property
    def old_hard_time_to(self):
        """Gets the old_hard_time_to of this FactEventWindowChanged.  # noqa: E501

        Previous end of the window.  # noqa: E501

        :return: The old_hard_time_to of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._old_hard_time_to

    @old_hard_time_to.setter
    def old_hard_time_to(self, old_hard_time_to):
        """Sets the old_hard_time_to of this FactEventWindowChanged.

        Previous end of the window.  # noqa: E501

        :param old_hard_time_to: The old_hard_time_to of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._old_hard_time_to = old_hard_time_to

    @property
    def old_soft_time_from(self):
        """Gets the old_soft_time_from of this FactEventWindowChanged.  # noqa: E501

        Previous start of the window.  # noqa: E501

        :return: The old_soft_time_from of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._old_soft_time_from

    @old_soft_time_from.setter
    def old_soft_time_from(self, old_soft_time_from):
        """Sets the old_soft_time_from of this FactEventWindowChanged.

        Previous start of the window.  # noqa: E501

        :param old_soft_time_from: The old_soft_time_from of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._old_soft_time_from = old_soft_time_from

    @property
    def old_soft_time_to(self):
        """Gets the old_soft_time_to of this FactEventWindowChanged.  # noqa: E501

        Previous end of the soft window.  # noqa: E501

        :return: The old_soft_time_to of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._old_soft_time_to

    @old_soft_time_to.setter
    def old_soft_time_to(self, old_soft_time_to):
        """Sets the old_soft_time_to of this FactEventWindowChanged.

        Previous end of the soft window.  # noqa: E501

        :param old_soft_time_to: The old_soft_time_to of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._old_soft_time_to = old_soft_time_to

    @property
    def new_hard_time_from(self):
        """Gets the new_hard_time_from of this FactEventWindowChanged.  # noqa: E501

        New start of the window.  # noqa: E501

        :return: The new_hard_time_from of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._new_hard_time_from

    @new_hard_time_from.setter
    def new_hard_time_from(self, new_hard_time_from):
        """Sets the new_hard_time_from of this FactEventWindowChanged.

        New start of the window.  # noqa: E501

        :param new_hard_time_from: The new_hard_time_from of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._new_hard_time_from = new_hard_time_from

    @property
    def new_hard_time_to(self):
        """Gets the new_hard_time_to of this FactEventWindowChanged.  # noqa: E501

        New end of the  window.  # noqa: E501

        :return: The new_hard_time_to of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._new_hard_time_to

    @new_hard_time_to.setter
    def new_hard_time_to(self, new_hard_time_to):
        """Sets the new_hard_time_to of this FactEventWindowChanged.

        New end of the  window.  # noqa: E501

        :param new_hard_time_to: The new_hard_time_to of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._new_hard_time_to = new_hard_time_to

    @property
    def new_soft_time_from(self):
        """Gets the new_soft_time_from of this FactEventWindowChanged.  # noqa: E501

        New start of the soft window.  # noqa: E501

        :return: The new_soft_time_from of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._new_soft_time_from

    @new_soft_time_from.setter
    def new_soft_time_from(self, new_soft_time_from):
        """Sets the new_soft_time_from of this FactEventWindowChanged.

        New start of the soft window.  # noqa: E501

        :param new_soft_time_from: The new_soft_time_from of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._new_soft_time_from = new_soft_time_from

    @property
    def new_soft_time_to(self):
        """Gets the new_soft_time_to of this FactEventWindowChanged.  # noqa: E501

        New end of the soft window.  # noqa: E501

        :return: The new_soft_time_to of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._new_soft_time_to

    @new_soft_time_to.setter
    def new_soft_time_to(self, new_soft_time_to):
        """Sets the new_soft_time_to of this FactEventWindowChanged.

        New end of the soft window.  # noqa: E501

        :param new_soft_time_to: The new_soft_time_to of this FactEventWindowChanged.  # noqa: E501
        :type: datetime
        """

        self._new_soft_time_to = new_soft_time_to

    @property
    def window_change_reason(self):
        """Gets the window_change_reason of this FactEventWindowChanged.  # noqa: E501

        Reason for soft window change.  # noqa: E501

        :return: The window_change_reason of this FactEventWindowChanged.  # noqa: E501
        :rtype: str
        """
        return self._window_change_reason

    @window_change_reason.setter
    def window_change_reason(self, window_change_reason):
        """Sets the window_change_reason of this FactEventWindowChanged.

        Reason for soft window change.  # noqa: E501

        :param window_change_reason: The window_change_reason of this FactEventWindowChanged.  # noqa: E501
        :type: str
        """

        self._window_change_reason = window_change_reason

    @property
    def fact_time(self):
        """Gets the fact_time of this FactEventWindowChanged.  # noqa: E501

        Fact time in the [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :return: The fact_time of this FactEventWindowChanged.  # noqa: E501
        :rtype: datetime
        """
        return self._fact_time

    @fact_time.setter
    def fact_time(self, fact_time):
        """Sets the fact_time of this FactEventWindowChanged.

        Fact time in the [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6) format.  # noqa: E501

        :param fact_time: The fact_time of this FactEventWindowChanged.  # noqa: E501
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
        if not isinstance(other, FactEventWindowChanged):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, FactEventWindowChanged):
            return True

        return self.to_dict() != other.to_dict()
