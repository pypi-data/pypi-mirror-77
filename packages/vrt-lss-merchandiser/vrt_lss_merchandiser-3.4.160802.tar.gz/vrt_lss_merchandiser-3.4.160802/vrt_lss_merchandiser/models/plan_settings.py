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


class PlanSettings(object):
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
        'configuration': 'str',
        'planning_time': 'int',
        'result_ttl': 'int',
        'result_timezone': 'int',
        'predict_slots': 'int',
        'transport_factor': 'list[TransportFactor]',
        'capacity_factor': 'list[CapacityFactor]',
        'routing': 'list[Routing]',
        'assumptions': 'PlanAssumptions',
        'precision': 'int'
    }

    attribute_map = {
        'configuration': 'configuration',
        'planning_time': 'planning_time',
        'result_ttl': 'result_ttl',
        'result_timezone': 'result_timezone',
        'predict_slots': 'predict_slots',
        'transport_factor': 'transport_factor',
        'capacity_factor': 'capacity_factor',
        'routing': 'routing',
        'assumptions': 'assumptions',
        'precision': 'precision'
    }

    def __init__(self, configuration='default', planning_time=20, result_ttl=20, result_timezone=0, predict_slots=0, transport_factor=[], capacity_factor=[], routing=[], assumptions=None, precision=2, local_vars_configuration=None):  # noqa: E501
        """PlanSettings - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._configuration = None
        self._planning_time = None
        self._result_ttl = None
        self._result_timezone = None
        self._predict_slots = None
        self._transport_factor = None
        self._capacity_factor = None
        self._routing = None
        self._assumptions = None
        self._precision = None
        self.discriminator = None

        if configuration is not None:
            self.configuration = configuration
        if planning_time is not None:
            self.planning_time = planning_time
        if result_ttl is not None:
            self.result_ttl = result_ttl
        if result_timezone is not None:
            self.result_timezone = result_timezone
        if predict_slots is not None:
            self.predict_slots = predict_slots
        if transport_factor is not None:
            self.transport_factor = transport_factor
        if capacity_factor is not None:
            self.capacity_factor = capacity_factor
        if routing is not None:
            self.routing = routing
        if assumptions is not None:
            self.assumptions = assumptions
        if precision is not None:
            self.precision = precision

    @property
    def configuration(self):
        """Gets the configuration of this PlanSettings.  # noqa: E501

        Name of the planning configuration. The configuration determines the result goal and quality. [List of available](https://docs.veeroute.com/#/lss/scenarios?id=Конфигурация-планирования) planning configurations.   # noqa: E501

        :return: The configuration of this PlanSettings.  # noqa: E501
        :rtype: str
        """
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        """Sets the configuration of this PlanSettings.

        Name of the planning configuration. The configuration determines the result goal and quality. [List of available](https://docs.veeroute.com/#/lss/scenarios?id=Конфигурация-планирования) planning configurations.   # noqa: E501

        :param configuration: The configuration of this PlanSettings.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                configuration is not None and len(configuration) > 1000):
            raise ValueError("Invalid value for `configuration`, length must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                configuration is not None and len(configuration) < 1):
            raise ValueError("Invalid value for `configuration`, length must be greater than or equal to `1`")  # noqa: E501

        self._configuration = configuration

    @property
    def planning_time(self):
        """Gets the planning_time of this PlanSettings.  # noqa: E501

        Planning time in minutes. The countdown starts from the time when data is uploaded to the server and planning starts.   # noqa: E501

        :return: The planning_time of this PlanSettings.  # noqa: E501
        :rtype: int
        """
        return self._planning_time

    @planning_time.setter
    def planning_time(self, planning_time):
        """Sets the planning_time of this PlanSettings.

        Planning time in minutes. The countdown starts from the time when data is uploaded to the server and planning starts.   # noqa: E501

        :param planning_time: The planning_time of this PlanSettings.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                planning_time is not None and planning_time > 2880):  # noqa: E501
            raise ValueError("Invalid value for `planning_time`, must be a value less than or equal to `2880`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                planning_time is not None and planning_time < 1):  # noqa: E501
            raise ValueError("Invalid value for `planning_time`, must be a value greater than or equal to `1`")  # noqa: E501

        self._planning_time = planning_time

    @property
    def result_ttl(self):
        """Gets the result_ttl of this PlanSettings.  # noqa: E501

        Planning result lifetime, in minutes. The countdown starts from the time when the planning is completed.   # noqa: E501

        :return: The result_ttl of this PlanSettings.  # noqa: E501
        :rtype: int
        """
        return self._result_ttl

    @result_ttl.setter
    def result_ttl(self, result_ttl):
        """Sets the result_ttl of this PlanSettings.

        Planning result lifetime, in minutes. The countdown starts from the time when the planning is completed.   # noqa: E501

        :param result_ttl: The result_ttl of this PlanSettings.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                result_ttl is not None and result_ttl > 14400):  # noqa: E501
            raise ValueError("Invalid value for `result_ttl`, must be a value less than or equal to `14400`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                result_ttl is not None and result_ttl < 1):  # noqa: E501
            raise ValueError("Invalid value for `result_ttl`, must be a value greater than or equal to `1`")  # noqa: E501

        self._result_ttl = result_ttl

    @property
    def result_timezone(self):
        """Gets the result_timezone of this PlanSettings.  # noqa: E501

        The time zone where the planning result is returned.   # noqa: E501

        :return: The result_timezone of this PlanSettings.  # noqa: E501
        :rtype: int
        """
        return self._result_timezone

    @result_timezone.setter
    def result_timezone(self, result_timezone):
        """Sets the result_timezone of this PlanSettings.

        The time zone where the planning result is returned.   # noqa: E501

        :param result_timezone: The result_timezone of this PlanSettings.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                result_timezone is not None and result_timezone > 12):  # noqa: E501
            raise ValueError("Invalid value for `result_timezone`, must be a value less than or equal to `12`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                result_timezone is not None and result_timezone < -12):  # noqa: E501
            raise ValueError("Invalid value for `result_timezone`, must be a value greater than or equal to `-12`")  # noqa: E501

        self._result_timezone = result_timezone

    @property
    def predict_slots(self):
        """Gets the predict_slots of this PlanSettings.  # noqa: E501

        The number of slots for data preparation to predict time windows. If the value equals zero, the data to predict time windows is not prepared. Learn more about the [time window tip script](https://docs.veeroute.com/#/lss/scenarios?id=Подсказка-временных-окон).   # noqa: E501

        :return: The predict_slots of this PlanSettings.  # noqa: E501
        :rtype: int
        """
        return self._predict_slots

    @predict_slots.setter
    def predict_slots(self, predict_slots):
        """Sets the predict_slots of this PlanSettings.

        The number of slots for data preparation to predict time windows. If the value equals zero, the data to predict time windows is not prepared. Learn more about the [time window tip script](https://docs.veeroute.com/#/lss/scenarios?id=Подсказка-временных-окон).   # noqa: E501

        :param predict_slots: The predict_slots of this PlanSettings.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                predict_slots is not None and predict_slots > 4):  # noqa: E501
            raise ValueError("Invalid value for `predict_slots`, must be a value less than or equal to `4`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                predict_slots is not None and predict_slots < 0):  # noqa: E501
            raise ValueError("Invalid value for `predict_slots`, must be a value greater than or equal to `0`")  # noqa: E501

        self._predict_slots = predict_slots

    @property
    def transport_factor(self):
        """Gets the transport_factor of this PlanSettings.  # noqa: E501

        Vehicle speed change coefficients.  # noqa: E501

        :return: The transport_factor of this PlanSettings.  # noqa: E501
        :rtype: list[TransportFactor]
        """
        return self._transport_factor

    @transport_factor.setter
    def transport_factor(self, transport_factor):
        """Sets the transport_factor of this PlanSettings.

        Vehicle speed change coefficients.  # noqa: E501

        :param transport_factor: The transport_factor of this PlanSettings.  # noqa: E501
        :type: list[TransportFactor]
        """

        self._transport_factor = transport_factor

    @property
    def capacity_factor(self):
        """Gets the capacity_factor of this PlanSettings.  # noqa: E501

        Vehicle capacity change coefficients.  # noqa: E501

        :return: The capacity_factor of this PlanSettings.  # noqa: E501
        :rtype: list[CapacityFactor]
        """
        return self._capacity_factor

    @capacity_factor.setter
    def capacity_factor(self, capacity_factor):
        """Sets the capacity_factor of this PlanSettings.

        Vehicle capacity change coefficients.  # noqa: E501

        :param capacity_factor: The capacity_factor of this PlanSettings.  # noqa: E501
        :type: list[CapacityFactor]
        """

        self._capacity_factor = capacity_factor

    @property
    def routing(self):
        """Gets the routing of this PlanSettings.  # noqa: E501

        Time and distance matrices list for each vehicle type. By specifying an external routing matrix, parameters `flight_distance`, `traffic_jams`, `transport_factor` are not taken into account.   # noqa: E501

        :return: The routing of this PlanSettings.  # noqa: E501
        :rtype: list[Routing]
        """
        return self._routing

    @routing.setter
    def routing(self, routing):
        """Sets the routing of this PlanSettings.

        Time and distance matrices list for each vehicle type. By specifying an external routing matrix, parameters `flight_distance`, `traffic_jams`, `transport_factor` are not taken into account.   # noqa: E501

        :param routing: The routing of this PlanSettings.  # noqa: E501
        :type: list[Routing]
        """

        self._routing = routing

    @property
    def assumptions(self):
        """Gets the assumptions of this PlanSettings.  # noqa: E501


        :return: The assumptions of this PlanSettings.  # noqa: E501
        :rtype: PlanAssumptions
        """
        return self._assumptions

    @assumptions.setter
    def assumptions(self, assumptions):
        """Sets the assumptions of this PlanSettings.


        :param assumptions: The assumptions of this PlanSettings.  # noqa: E501
        :type: PlanAssumptions
        """

        self._assumptions = assumptions

    @property
    def precision(self):
        """Gets the precision of this PlanSettings.  # noqa: E501

        Specifies the calculation accuracy in the decimal point sequence number. It equals 2 by default, so the accuracy is 0.01.   # noqa: E501

        :return: The precision of this PlanSettings.  # noqa: E501
        :rtype: int
        """
        return self._precision

    @precision.setter
    def precision(self, precision):
        """Sets the precision of this PlanSettings.

        Specifies the calculation accuracy in the decimal point sequence number. It equals 2 by default, so the accuracy is 0.01.   # noqa: E501

        :param precision: The precision of this PlanSettings.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                precision is not None and precision > 6):  # noqa: E501
            raise ValueError("Invalid value for `precision`, must be a value less than or equal to `6`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                precision is not None and precision < 0):  # noqa: E501
            raise ValueError("Invalid value for `precision`, must be a value greater than or equal to `0`")  # noqa: E501

        self._precision = precision

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
        if not isinstance(other, PlanSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanSettings):
            return True

        return self.to_dict() != other.to_dict()
