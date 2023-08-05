# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.08.17
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from agilicus_api.configuration import Configuration


class TokenValidity(object):
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
        'start': 'datetime',
        'duration': 'int',
        'end': 'datetime'
    }

    attribute_map = {
        'start': 'start',
        'duration': 'duration',
        'end': 'end'
    }

    def __init__(self, start=None, duration=None, end=None, local_vars_configuration=None):  # noqa: E501
        """TokenValidity - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._start = None
        self._duration = None
        self._end = None
        self.discriminator = None

        if start is not None:
            self.start = start
        if duration is not None:
            self.duration = duration
        if end is not None:
            self.end = end

    @property
    def start(self):
        """Gets the start of this TokenValidity.  # noqa: E501

        The start time for when the token is valid  # noqa: E501

        :return: The start of this TokenValidity.  # noqa: E501
        :rtype: datetime
        """
        return self._start

    @start.setter
    def start(self, start):
        """Sets the start of this TokenValidity.

        The start time for when the token is valid  # noqa: E501

        :param start: The start of this TokenValidity.  # noqa: E501
        :type: datetime
        """

        self._start = start

    @property
    def duration(self):
        """Gets the duration of this TokenValidity.  # noqa: E501

        The duration of time for which the token is valid  # noqa: E501

        :return: The duration of this TokenValidity.  # noqa: E501
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this TokenValidity.

        The duration of time for which the token is valid  # noqa: E501

        :param duration: The duration of this TokenValidity.  # noqa: E501
        :type: int
        """

        self._duration = duration

    @property
    def end(self):
        """Gets the end of this TokenValidity.  # noqa: E501

        The end time for when the token is valid  # noqa: E501

        :return: The end of this TokenValidity.  # noqa: E501
        :rtype: datetime
        """
        return self._end

    @end.setter
    def end(self, end):
        """Sets the end of this TokenValidity.

        The end time for when the token is valid  # noqa: E501

        :param end: The end of this TokenValidity.  # noqa: E501
        :type: datetime
        """

        self._end = end

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
        if not isinstance(other, TokenValidity):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TokenValidity):
            return True

        return self.to_dict() != other.to_dict()
