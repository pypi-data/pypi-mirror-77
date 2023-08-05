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


class CapacityFactor(object):
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
        'transport_type': 'TransportType',
        'capacity': 'Capacity'
    }

    attribute_map = {
        'transport_type': 'transport_type',
        'capacity': 'capacity'
    }

    def __init__(self, transport_type=None, capacity=None, local_vars_configuration=None):  # noqa: E501
        """CapacityFactor - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._transport_type = None
        self._capacity = None
        self.discriminator = None

        self.transport_type = transport_type
        self.capacity = capacity

    @property
    def transport_type(self):
        """Gets the transport_type of this CapacityFactor.  # noqa: E501


        :return: The transport_type of this CapacityFactor.  # noqa: E501
        :rtype: TransportType
        """
        return self._transport_type

    @transport_type.setter
    def transport_type(self, transport_type):
        """Sets the transport_type of this CapacityFactor.


        :param transport_type: The transport_type of this CapacityFactor.  # noqa: E501
        :type: TransportType
        """
        if self.local_vars_configuration.client_side_validation and transport_type is None:  # noqa: E501
            raise ValueError("Invalid value for `transport_type`, must not be `None`")  # noqa: E501

        self._transport_type = transport_type

    @property
    def capacity(self):
        """Gets the capacity of this CapacityFactor.  # noqa: E501


        :return: The capacity of this CapacityFactor.  # noqa: E501
        :rtype: Capacity
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this CapacityFactor.


        :param capacity: The capacity of this CapacityFactor.  # noqa: E501
        :type: Capacity
        """

        self._capacity = capacity

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
        if not isinstance(other, CapacityFactor):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CapacityFactor):
            return True

        return self.to_dict() != other.to_dict()
