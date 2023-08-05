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


class PlanId(object):
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
        'tracedata': 'TraceData',
        'id': 'str'
    }

    attribute_map = {
        'tracedata': 'tracedata',
        'id': 'id'
    }

    def __init__(self, tracedata=None, id=None, local_vars_configuration=None):  # noqa: E501
        """PlanId - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._tracedata = None
        self._id = None
        self.discriminator = None

        if tracedata is not None:
            self.tracedata = tracedata
        self.id = id

    @property
    def tracedata(self):
        """Gets the tracedata of this PlanId.  # noqa: E501


        :return: The tracedata of this PlanId.  # noqa: E501
        :rtype: TraceData
        """
        return self._tracedata

    @tracedata.setter
    def tracedata(self, tracedata):
        """Sets the tracedata of this PlanId.


        :param tracedata: The tracedata of this PlanId.  # noqa: E501
        :type: TraceData
        """

        self._tracedata = tracedata

    @property
    def id(self):
        """Gets the id of this PlanId.  # noqa: E501

        Calculation ID.  # noqa: E501

        :return: The id of this PlanId.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PlanId.

        Calculation ID.  # noqa: E501

        :param id: The id of this PlanId.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

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
        if not isinstance(other, PlanId):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PlanId):
            return True

        return self.to_dict() != other.to_dict()
