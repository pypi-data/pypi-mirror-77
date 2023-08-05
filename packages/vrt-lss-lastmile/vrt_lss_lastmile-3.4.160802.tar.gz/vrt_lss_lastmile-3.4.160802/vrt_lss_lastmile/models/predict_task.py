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


class PredictTask(object):
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
        'id': 'str',
        'order': 'Order',
        'locations': 'list[AdvancedLocation]'
    }

    attribute_map = {
        'id': 'id',
        'order': 'order',
        'locations': 'locations'
    }

    def __init__(self, id=None, order=None, locations=None, local_vars_configuration=None):  # noqa: E501
        """PredictTask - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._order = None
        self._locations = None
        self.discriminator = None

        self.id = id
        self.order = order
        self.locations = locations

    @property
    def id(self):
        """Gets the id of this PredictTask.  # noqa: E501

        Calculation ID.  # noqa: E501

        :return: The id of this PredictTask.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PredictTask.

        Calculation ID.  # noqa: E501

        :param id: The id of this PredictTask.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def order(self):
        """Gets the order of this PredictTask.  # noqa: E501


        :return: The order of this PredictTask.  # noqa: E501
        :rtype: Order
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this PredictTask.


        :param order: The order of this PredictTask.  # noqa: E501
        :type: Order
        """
        if self.local_vars_configuration.client_side_validation and order is None:  # noqa: E501
            raise ValueError("Invalid value for `order`, must not be `None`")  # noqa: E501

        self._order = order

    @property
    def locations(self):
        """Gets the locations of this PredictTask.  # noqa: E501

        List of locations used in the order for window prediction.  # noqa: E501

        :return: The locations of this PredictTask.  # noqa: E501
        :rtype: list[AdvancedLocation]
        """
        return self._locations

    @locations.setter
    def locations(self, locations):
        """Sets the locations of this PredictTask.

        List of locations used in the order for window prediction.  # noqa: E501

        :param locations: The locations of this PredictTask.  # noqa: E501
        :type: list[AdvancedLocation]
        """
        if self.local_vars_configuration.client_side_validation and locations is None:  # noqa: E501
            raise ValueError("Invalid value for `locations`, must not be `None`")  # noqa: E501

        self._locations = locations

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
        if not isinstance(other, PredictTask):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PredictTask):
            return True

        return self.to_dict() != other.to_dict()
