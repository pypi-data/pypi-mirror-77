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


class Cargo(object):
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
        'capacity': 'Capacity',
        'width': 'float',
        'height': 'float',
        'length': 'float',
        'max_storage_time': 'int',
        'restrictions': 'list[str]'
    }

    attribute_map = {
        'key': 'key',
        'capacity': 'capacity',
        'width': 'width',
        'height': 'height',
        'length': 'length',
        'max_storage_time': 'max_storage_time',
        'restrictions': 'restrictions'
    }

    def __init__(self, key=None, capacity=None, width=0, height=0, length=0, max_storage_time=43800, restrictions=None, local_vars_configuration=None):  # noqa: E501
        """Cargo - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._capacity = None
        self._width = None
        self._height = None
        self._length = None
        self._max_storage_time = None
        self._restrictions = None
        self.discriminator = None

        self.key = key
        self.capacity = capacity
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if length is not None:
            self.length = length
        if max_storage_time is not None:
            self.max_storage_time = max_storage_time
        if restrictions is not None:
            self.restrictions = restrictions

    @property
    def key(self):
        """Gets the key of this Cargo.  # noqa: E501

        Cargo key, unique ID.  # noqa: E501

        :return: The key of this Cargo.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Cargo.

        Cargo key, unique ID.  # noqa: E501

        :param key: The key of this Cargo.  # noqa: E501
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
    def capacity(self):
        """Gets the capacity of this Cargo.  # noqa: E501


        :return: The capacity of this Cargo.  # noqa: E501
        :rtype: Capacity
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this Cargo.


        :param capacity: The capacity of this Cargo.  # noqa: E501
        :type: Capacity
        """

        self._capacity = capacity

    @property
    def width(self):
        """Gets the width of this Cargo.  # noqa: E501

        Width in meters, used to check the vehicle compartment capacity.  # noqa: E501

        :return: The width of this Cargo.  # noqa: E501
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this Cargo.

        Width in meters, used to check the vehicle compartment capacity.  # noqa: E501

        :param width: The width of this Cargo.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                width is not None and width > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `width`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                width is not None and width < 0):  # noqa: E501
            raise ValueError("Invalid value for `width`, must be a value greater than or equal to `0`")  # noqa: E501

        self._width = width

    @property
    def height(self):
        """Gets the height of this Cargo.  # noqa: E501

        Height in meters, used to check the vehicle compartment capacity.  # noqa: E501

        :return: The height of this Cargo.  # noqa: E501
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Cargo.

        Height in meters, used to check the vehicle compartment capacity.  # noqa: E501

        :param height: The height of this Cargo.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                height is not None and height > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `height`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                height is not None and height < 0):  # noqa: E501
            raise ValueError("Invalid value for `height`, must be a value greater than or equal to `0`")  # noqa: E501

        self._height = height

    @property
    def length(self):
        """Gets the length of this Cargo.  # noqa: E501

        Length in meters, used to check the vehicle compartment capacity.  # noqa: E501

        :return: The length of this Cargo.  # noqa: E501
        :rtype: float
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Cargo.

        Length in meters, used to check the vehicle compartment capacity.  # noqa: E501

        :param length: The length of this Cargo.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                length is not None and length > 1000000):  # noqa: E501
            raise ValueError("Invalid value for `length`, must be a value less than or equal to `1000000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                length is not None and length < 0):  # noqa: E501
            raise ValueError("Invalid value for `length`, must be a value greater than or equal to `0`")  # noqa: E501

        self._length = length

    @property
    def max_storage_time(self):
        """Gets the max_storage_time of this Cargo.  # noqa: E501

        The maximum time for cargo storage on the vehicle, in minutes.  If not specified, the constraint is not taken into account.   # noqa: E501

        :return: The max_storage_time of this Cargo.  # noqa: E501
        :rtype: int
        """
        return self._max_storage_time

    @max_storage_time.setter
    def max_storage_time(self, max_storage_time):
        """Sets the max_storage_time of this Cargo.

        The maximum time for cargo storage on the vehicle, in minutes.  If not specified, the constraint is not taken into account.   # noqa: E501

        :param max_storage_time: The max_storage_time of this Cargo.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                max_storage_time is not None and max_storage_time > 43800):  # noqa: E501
            raise ValueError("Invalid value for `max_storage_time`, must be a value less than or equal to `43800`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_storage_time is not None and max_storage_time < 0):  # noqa: E501
            raise ValueError("Invalid value for `max_storage_time`, must be a value greater than or equal to `0`")  # noqa: E501

        self._max_storage_time = max_storage_time

    @property
    def restrictions(self):
        """Gets the restrictions of this Cargo.  # noqa: E501

        List of necessary requirements for a cargo compartment.  # noqa: E501

        :return: The restrictions of this Cargo.  # noqa: E501
        :rtype: list[str]
        """
        return self._restrictions

    @restrictions.setter
    def restrictions(self, restrictions):
        """Sets the restrictions of this Cargo.

        List of necessary requirements for a cargo compartment.  # noqa: E501

        :param restrictions: The restrictions of this Cargo.  # noqa: E501
        :type: list[str]
        """

        self._restrictions = restrictions

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
        if not isinstance(other, Cargo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Cargo):
            return True

        return self.to_dict() != other.to_dict()
