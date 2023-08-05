# coding: utf-8

"""
    VeeRoute.LSS Merchandiser

    VeeRoute.LSS Merchandiser API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from vrt_lss_merchandiser.configuration import Configuration


class PlanAssumptions(object):
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
        'traffic_jams': 'bool',
        'flight_distance': 'bool',
        'disable_compatibility': 'bool',
        'disable_capacity': 'bool',
        'same_order_time_window': 'bool',
        'expand_shift_time_window': 'bool'
    }

    attribute_map = {
        'traffic_jams': 'traffic_jams',
        'flight_distance': 'flight_distance',
        'disable_compatibility': 'disable_compatibility',
        'disable_capacity': 'disable_capacity',
        'same_order_time_window': 'same_order_time_window',
        'expand_shift_time_window': 'expand_shift_time_window'
    }

    def __init__(self, traffic_jams=True, flight_distance=False, disable_compatibility=False, disable_capacity=False, same_order_time_window=False, expand_shift_time_window=False, local_vars_configuration=None):  # noqa: E501
        """PlanAssumptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._traffic_jams = None
        self._flight_distance = None
        self._disable_compatibility = None
        self._disable_capacity = None
        self._same_order_time_window = None
        self._expand_shift_time_window = None
        self.discriminator = None

        if traffic_jams is not None:
            self.traffic_jams = traffic_jams
        if flight_distance is not None:
            self.flight_distance = flight_distance
        if disable_compatibility is not None:
            self.disable_compatibility = disable_compatibility
        if disable_capacity is not None:
            self.disable_capacity = disable_capacity
        if same_order_time_window is not None:
            self.same_order_time_window = same_order_time_window
        if expand_shift_time_window is not None:
            self.expand_shift_time_window = expand_shift_time_window

    @property
    def traffic_jams(self):
        """Gets the traffic_jams of this PlanAssumptions.  # noqa: E501

        Accounting for traffic during the route planning.  # noqa: E501

        :return: The traffic_jams of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._traffic_jams

    @traffic_jams.setter
    def traffic_jams(self, traffic_jams):
        """Sets the traffic_jams of this PlanAssumptions.

        Accounting for traffic during the route planning.  # noqa: E501

        :param traffic_jams: The traffic_jams of this PlanAssumptions.  # noqa: E501
        :type: bool
        """

        self._traffic_jams = traffic_jams

    @property
    def flight_distance(self):
        """Gets the flight_distance of this PlanAssumptions.  # noqa: E501

        Use for calculating straight line distances. If `false` is specified, distances are calculated by roads. When this parameter is enabled, traffic tracking (`traffic_jams`) is automatically disabled.   # noqa: E501

        :return: The flight_distance of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._flight_distance

    @flight_distance.setter
    def flight_distance(self, flight_distance):
        """Sets the flight_distance of this PlanAssumptions.

        Use for calculating straight line distances. If `false` is specified, distances are calculated by roads. When this parameter is enabled, traffic tracking (`traffic_jams`) is automatically disabled.   # noqa: E501

        :param flight_distance: The flight_distance of this PlanAssumptions.  # noqa: E501
        :type: bool
        """

        self._flight_distance = flight_distance

    @property
    def disable_compatibility(self):
        """Gets the disable_compatibility of this PlanAssumptions.  # noqa: E501

        Disable the accounting for capacity. If `true` is specified, all becomes compatible with everything.   # noqa: E501

        :return: The disable_compatibility of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._disable_compatibility

    @disable_compatibility.setter
    def disable_compatibility(self, disable_compatibility):
        """Sets the disable_compatibility of this PlanAssumptions.

        Disable the accounting for capacity. If `true` is specified, all becomes compatible with everything.   # noqa: E501

        :param disable_compatibility: The disable_compatibility of this PlanAssumptions.  # noqa: E501
        :type: bool
        """

        self._disable_compatibility = disable_compatibility

    @property
    def disable_capacity(self):
        """Gets the disable_capacity of this PlanAssumptions.  # noqa: E501

        Disable the accounting for capacity. If `true` is specified, all vehicles can accommodate an unlimited cargo amount.   # noqa: E501

        :return: The disable_capacity of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._disable_capacity

    @disable_capacity.setter
    def disable_capacity(self, disable_capacity):
        """Sets the disable_capacity of this PlanAssumptions.

        Disable the accounting for capacity. If `true` is specified, all vehicles can accommodate an unlimited cargo amount.   # noqa: E501

        :param disable_capacity: The disable_capacity of this PlanAssumptions.  # noqa: E501
        :type: bool
        """

        self._disable_capacity = disable_capacity

    @property
    def same_order_time_window(self):
        """Gets the same_order_time_window of this PlanAssumptions.  # noqa: E501

        Use for calculation the same (specified) time window for orders and demands. The time window is specified from the beginning of the earliest window to the end of the latest window from all orders and demands.   # noqa: E501

        :return: The same_order_time_window of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._same_order_time_window

    @same_order_time_window.setter
    def same_order_time_window(self, same_order_time_window):
        """Sets the same_order_time_window of this PlanAssumptions.

        Use for calculation the same (specified) time window for orders and demands. The time window is specified from the beginning of the earliest window to the end of the latest window from all orders and demands.   # noqa: E501

        :param same_order_time_window: The same_order_time_window of this PlanAssumptions.  # noqa: E501
        :type: bool
        """

        self._same_order_time_window = same_order_time_window

    @property
    def expand_shift_time_window(self):
        """Gets the expand_shift_time_window of this PlanAssumptions.  # noqa: E501

        Expand the time window for performers' and vehicle shifts.  The left border of the first shift extends to the left border of the specified window, right border extends to the right border or to the beginning of the next window for this entity. Each next shift moves the right border to the next shift or to the right border of the specified window.   # noqa: E501

        :return: The expand_shift_time_window of this PlanAssumptions.  # noqa: E501
        :rtype: bool
        """
        return self._expand_shift_time_window

    @expand_shift_time_window.setter
    def expand_shift_time_window(self, expand_shift_time_window):
        """Sets the expand_shift_time_window of this PlanAssumptions.

        Expand the time window for performers' and vehicle shifts.  The left border of the first shift extends to the left border of the specified window, right border extends to the right border or to the beginning of the next window for this entity. Each next shift moves the right border to the next shift or to the right border of the specified window.   # noqa: E501

        :param expand_shift_time_window: The expand_shift_time_window of this PlanAssumptions.  # noqa: E501
        :type: bool
        """

        self._expand_shift_time_window = expand_shift_time_window

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
        if not isinstance(other, PlanAssumptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanAssumptions):
            return True

        return self.to_dict() != other.to_dict()
