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


class Box(object):
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
        'max_size': 'Capacity',
        'width': 'float',
        'height': 'float',
        'length': 'float',
        'features': 'list[str]'
    }

    attribute_map = {
        'key': 'key',
        'capacity': 'capacity',
        'max_size': 'max_size',
        'width': 'width',
        'height': 'height',
        'length': 'length',
        'features': 'features'
    }

    def __init__(self, key=None, capacity=None, max_size=None, width=0, height=0, length=0, features=None, local_vars_configuration=None):  # noqa: E501
        """Box - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._key = None
        self._capacity = None
        self._max_size = None
        self._width = None
        self._height = None
        self._length = None
        self._features = None
        self.discriminator = None

        self.key = key
        self.capacity = capacity
        self.max_size = max_size
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if length is not None:
            self.length = length
        if features is not None:
            self.features = features

    @property
    def key(self):
        """Gets the key of this Box.  # noqa: E501

        Compartment key, a unique ID used to identify the cargo placement in compartments.  # noqa: E501

        :return: The key of this Box.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Box.

        Compartment key, a unique ID used to identify the cargo placement in compartments.  # noqa: E501

        :param key: The key of this Box.  # noqa: E501
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
        """Gets the capacity of this Box.  # noqa: E501


        :return: The capacity of this Box.  # noqa: E501
        :rtype: Capacity
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this Box.


        :param capacity: The capacity of this Box.  # noqa: E501
        :type: Capacity
        """

        self._capacity = capacity

    @property
    def max_size(self):
        """Gets the max_size of this Box.  # noqa: E501


        :return: The max_size of this Box.  # noqa: E501
        :rtype: Capacity
        """
        return self._max_size

    @max_size.setter
    def max_size(self, max_size):
        """Sets the max_size of this Box.


        :param max_size: The max_size of this Box.  # noqa: E501
        :type: Capacity
        """

        self._max_size = max_size

    @property
    def width(self):
        """Gets the width of this Box.  # noqa: E501

        Width in meters.  # noqa: E501

        :return: The width of this Box.  # noqa: E501
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width):
        """Sets the width of this Box.

        Width in meters.  # noqa: E501

        :param width: The width of this Box.  # noqa: E501
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
        """Gets the height of this Box.  # noqa: E501

        Height in meters.  # noqa: E501

        :return: The height of this Box.  # noqa: E501
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Box.

        Height in meters.  # noqa: E501

        :param height: The height of this Box.  # noqa: E501
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
        """Gets the length of this Box.  # noqa: E501

        Length in meters.  # noqa: E501

        :return: The length of this Box.  # noqa: E501
        :rtype: float
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Box.

        Length in meters.  # noqa: E501

        :param length: The length of this Box.  # noqa: E501
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
    def features(self):
        """Gets the features of this Box.  # noqa: E501

        Compartment features list that determines compatibility with the cargo.  # noqa: E501

        :return: The features of this Box.  # noqa: E501
        :rtype: list[str]
        """
        return self._features

    @features.setter
    def features(self, features):
        """Sets the features of this Box.

        Compartment features list that determines compatibility with the cargo.  # noqa: E501

        :param features: The features of this Box.  # noqa: E501
        :type: list[str]
        """

        self._features = features

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
        if not isinstance(other, Box):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Box):
            return True

        return self.to_dict() != other.to_dict()
