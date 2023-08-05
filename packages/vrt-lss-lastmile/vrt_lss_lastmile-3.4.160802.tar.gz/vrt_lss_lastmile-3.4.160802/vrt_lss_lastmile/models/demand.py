# coding: utf-8

"""
    VeeRoute.LSS Lastmile

    VeeRoute.LSS Lastmile API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from vrt_lss_lastmile.configuration import Configuration


class Demand(object):
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
        'key': 'str',
        'demand_type': 'str',
        'target_cargos': 'list[str]',
        'precedence_in_trip': 'int',
        'precedence_in_order': 'int',
        'possible_events': 'list[PossibleEvent]'
    }

    attribute_map = {
        'key': 'key',
        'demand_type': 'demand_type',
        'target_cargos': 'target_cargos',
        'precedence_in_trip': 'precedence_in_trip',
        'precedence_in_order': 'precedence_in_order',
        'possible_events': 'possible_events'
    }

    def __init__(self, key=None, demand_type=None, target_cargos=None, precedence_in_trip=0, precedence_in_order=0, possible_events=None, local_vars_configuration=None):  # noqa: E501
        """Demand - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._demand_type = None
        self._target_cargos = None
        self._precedence_in_trip = None
        self._precedence_in_order = None
        self._possible_events = None
        self.discriminator = None

        self.key = key
        self.demand_type = demand_type
        if target_cargos is not None:
            self.target_cargos = target_cargos
        if precedence_in_trip is not None:
            self.precedence_in_trip = precedence_in_trip
        if precedence_in_order is not None:
            self.precedence_in_order = precedence_in_order
        self.possible_events = possible_events

    @property
    def key(self):
        """Gets the key of this Demand.  # noqa: E501

        Location key, unique ID.  # noqa: E501

        :return: The key of this Demand.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Demand.

        Location key, unique ID.  # noqa: E501

        :param key: The key of this Demand.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and key is None:  # noqa: E501
            raise ValueError("Invalid value for `key`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) > 1024):
            raise ValueError("Invalid value for `key`, length must be less than or equal to `1024`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                key is not None and len(key) < 1):
            raise ValueError("Invalid value for `key`, length must be greater than or equal to `1`")  # noqa: E501

        self._key = key

    @property
    def demand_type(self):
        """Gets the demand_type of this Demand.  # noqa: E501

        The demand types are loading (`PICKUP`), unloading (`DROP`), work at the location (`WORK`).  # noqa: E501

        :return: The demand_type of this Demand.  # noqa: E501
        :rtype: str
        """
        return self._demand_type

    @demand_type.setter
    def demand_type(self, demand_type):
        """Sets the demand_type of this Demand.

        The demand types are loading (`PICKUP`), unloading (`DROP`), work at the location (`WORK`).  # noqa: E501

        :param demand_type: The demand_type of this Demand.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and demand_type is None:  # noqa: E501
            raise ValueError("Invalid value for `demand_type`, must not be `None`")  # noqa: E501
        allowed_values = ["PICKUP", "DROP", "WORK"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and demand_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `demand_type` ({0}), must be one of {1}"  # noqa: E501
                .format(demand_type, allowed_values)
            )

        self._demand_type = demand_type

    @property
    def target_cargos(self):
        """Gets the target_cargos of this Demand.  # noqa: E501

        Cargo keys list for `PICKUP`, one cargo key for  `DROP`, empty key for `WORK`.  # noqa: E501

        :return: The target_cargos of this Demand.  # noqa: E501
        :rtype: list[str]
        """
        return self._target_cargos

    @target_cargos.setter
    def target_cargos(self, target_cargos):
        """Sets the target_cargos of this Demand.

        Cargo keys list for `PICKUP`, one cargo key for  `DROP`, empty key for `WORK`.  # noqa: E501

        :param target_cargos: The target_cargos of this Demand.  # noqa: E501
        :type: list[str]
        """

        self._target_cargos = target_cargos

    @property
    def precedence_in_trip(self):
        """Gets the precedence_in_trip of this Demand.  # noqa: E501

        Precedence within a trip, 0 - the precedence is not taken into account.  # noqa: E501

        :return: The precedence_in_trip of this Demand.  # noqa: E501
        :rtype: int
        """
        return self._precedence_in_trip

    @precedence_in_trip.setter
    def precedence_in_trip(self, precedence_in_trip):
        """Sets the precedence_in_trip of this Demand.

        Precedence within a trip, 0 - the precedence is not taken into account.  # noqa: E501

        :param precedence_in_trip: The precedence_in_trip of this Demand.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                precedence_in_trip is not None and precedence_in_trip > 9000):  # noqa: E501
            raise ValueError("Invalid value for `precedence_in_trip`, must be a value less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                precedence_in_trip is not None and precedence_in_trip < 0):  # noqa: E501
            raise ValueError("Invalid value for `precedence_in_trip`, must be a value greater than or equal to `0`")  # noqa: E501

        self._precedence_in_trip = precedence_in_trip

    @property
    def precedence_in_order(self):
        """Gets the precedence_in_order of this Demand.  # noqa: E501

        Precedence within an order, 0 - the precedence is not taken into account.  # noqa: E501

        :return: The precedence_in_order of this Demand.  # noqa: E501
        :rtype: int
        """
        return self._precedence_in_order

    @precedence_in_order.setter
    def precedence_in_order(self, precedence_in_order):
        """Sets the precedence_in_order of this Demand.

        Precedence within an order, 0 - the precedence is not taken into account.  # noqa: E501

        :param precedence_in_order: The precedence_in_order of this Demand.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                precedence_in_order is not None and precedence_in_order > 9000):  # noqa: E501
            raise ValueError("Invalid value for `precedence_in_order`, must be a value less than or equal to `9000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                precedence_in_order is not None and precedence_in_order < 0):  # noqa: E501
            raise ValueError("Invalid value for `precedence_in_order`, must be a value greater than or equal to `0`")  # noqa: E501

        self._precedence_in_order = precedence_in_order

    @property
    def possible_events(self):
        """Gets the possible_events of this Demand.  # noqa: E501

        List of possible time windows and location keys to fulfil an order.  # noqa: E501

        :return: The possible_events of this Demand.  # noqa: E501
        :rtype: list[PossibleEvent]
        """
        return self._possible_events

    @possible_events.setter
    def possible_events(self, possible_events):
        """Sets the possible_events of this Demand.

        List of possible time windows and location keys to fulfil an order.  # noqa: E501

        :param possible_events: The possible_events of this Demand.  # noqa: E501
        :type: list[PossibleEvent]
        """
        if self.local_vars_configuration.client_side_validation and possible_events is None:  # noqa: E501
            raise ValueError("Invalid value for `possible_events`, must not be `None`")  # noqa: E501

        self._possible_events = possible_events

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
        if not isinstance(other, Demand):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Demand):
            return True

        return self.to_dict() != other.to_dict()
