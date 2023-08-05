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


class PlanTask(object):
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
        'performer': 'Performer',
        'orders': 'list[Order]',
        'settings': 'PlanSettings',
        'merchandiser_settings': 'MerchandiserSettings'
    }

    attribute_map = {
        'performer': 'performer',
        'orders': 'orders',
        'settings': 'settings',
        'merchandiser_settings': 'merchandiser_settings'
    }

    def __init__(self, performer=None, orders=None, settings=None, merchandiser_settings=None, local_vars_configuration=None):  # noqa: E501
        """PlanTask - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._performer = None
        self._orders = None
        self._settings = None
        self._merchandiser_settings = None
        self.discriminator = None

        self.performer = performer
        self.orders = orders
        if settings is not None:
            self.settings = settings
        if merchandiser_settings is not None:
            self.merchandiser_settings = merchandiser_settings

    @property
    def performer(self):
        """Gets the performer of this PlanTask.  # noqa: E501


        :return: The performer of this PlanTask.  # noqa: E501
        :rtype: Performer
        """
        return self._performer

    @performer.setter
    def performer(self, performer):
        """Sets the performer of this PlanTask.


        :param performer: The performer of this PlanTask.  # noqa: E501
        :type: Performer
        """
        if self.local_vars_configuration.client_side_validation and performer is None:  # noqa: E501
            raise ValueError("Invalid value for `performer`, must not be `None`")  # noqa: E501

        self._performer = performer

    @property
    def orders(self):
        """Gets the orders of this PlanTask.  # noqa: E501

        Orders list.  # noqa: E501

        :return: The orders of this PlanTask.  # noqa: E501
        :rtype: list[Order]
        """
        return self._orders

    @orders.setter
    def orders(self, orders):
        """Sets the orders of this PlanTask.

        Orders list.  # noqa: E501

        :param orders: The orders of this PlanTask.  # noqa: E501
        :type: list[Order]
        """
        if self.local_vars_configuration.client_side_validation and orders is None:  # noqa: E501
            raise ValueError("Invalid value for `orders`, must not be `None`")  # noqa: E501

        self._orders = orders

    @property
    def settings(self):
        """Gets the settings of this PlanTask.  # noqa: E501


        :return: The settings of this PlanTask.  # noqa: E501
        :rtype: PlanSettings
        """
        return self._settings

    @settings.setter
    def settings(self, settings):
        """Sets the settings of this PlanTask.


        :param settings: The settings of this PlanTask.  # noqa: E501
        :type: PlanSettings
        """

        self._settings = settings

    @property
    def merchandiser_settings(self):
        """Gets the merchandiser_settings of this PlanTask.  # noqa: E501


        :return: The merchandiser_settings of this PlanTask.  # noqa: E501
        :rtype: MerchandiserSettings
        """
        return self._merchandiser_settings

    @merchandiser_settings.setter
    def merchandiser_settings(self, merchandiser_settings):
        """Sets the merchandiser_settings of this PlanTask.


        :param merchandiser_settings: The merchandiser_settings of this PlanTask.  # noqa: E501
        :type: MerchandiserSettings
        """

        self._merchandiser_settings = merchandiser_settings

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
        if not isinstance(other, PlanTask):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanTask):
            return True

        return self.to_dict() != other.to_dict()
