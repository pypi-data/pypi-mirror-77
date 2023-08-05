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


class TripJob(object):
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
        'job_type': 'str',
        'job_time': 'datetime'
    }

    attribute_map = {
        'job_type': 'job_type',
        'job_time': 'job_time'
    }

    def __init__(self, job_type=None, job_time=None, local_vars_configuration=None):  # noqa: E501
        """TripJob - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._job_type = None
        self._job_time = None
        self.discriminator = None

        self.job_type = job_type
        self.job_time = job_time

    @property
    def job_type(self):
        """Gets the job_type of this TripJob.  # noqa: E501

        Possible work types:   * `LOCATION_ARRIVAL` - arrival at the location (finishing of the parking, allowed time window start).   * `READY_TO_WORK` - the performer is ready to work (finishing of waiting for the time window for work, waiting for location opening and demand time window start).   * `START_WORK` - getting started at the location (finishing of waiting for location opening, demand time window start, work start).   * `FINISH_WORK` - finish of work at the location (finishing of work, waiting for the suitable departure time to the next location).   * `LOCATION_DEPARTURE` - departure from the location.   # noqa: E501

        :return: The job_type of this TripJob.  # noqa: E501
        :rtype: str
        """
        return self._job_type

    @job_type.setter
    def job_type(self, job_type):
        """Sets the job_type of this TripJob.

        Possible work types:   * `LOCATION_ARRIVAL` - arrival at the location (finishing of the parking, allowed time window start).   * `READY_TO_WORK` - the performer is ready to work (finishing of waiting for the time window for work, waiting for location opening and demand time window start).   * `START_WORK` - getting started at the location (finishing of waiting for location opening, demand time window start, work start).   * `FINISH_WORK` - finish of work at the location (finishing of work, waiting for the suitable departure time to the next location).   * `LOCATION_DEPARTURE` - departure from the location.   # noqa: E501

        :param job_type: The job_type of this TripJob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and job_type is None:  # noqa: E501
            raise ValueError("Invalid value for `job_type`, must not be `None`")  # noqa: E501
        allowed_values = ["LOCATION_ARRIVAL", "READY_TO_WORK", "START_WORK", "FINISH_WORK", "LOCATION_DEPARTURE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and job_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `job_type` ({0}), must be one of {1}"  # noqa: E501
                .format(job_type, allowed_values)
            )

        self._job_type = job_type

    @property
    def job_time(self):
        """Gets the job_time of this TripJob.  # noqa: E501

        Start time according to the [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6).  # noqa: E501

        :return: The job_time of this TripJob.  # noqa: E501
        :rtype: datetime
        """
        return self._job_time

    @job_time.setter
    def job_time(self, job_time):
        """Sets the job_time of this TripJob.

        Start time according to the [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6).  # noqa: E501

        :param job_time: The job_time of this TripJob.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and job_time is None:  # noqa: E501
            raise ValueError("Invalid value for `job_time`, must not be `None`")  # noqa: E501

        self._job_time = job_time

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
        if not isinstance(other, TripJob):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TripJob):
            return True

        return self.to_dict() != other.to_dict()
