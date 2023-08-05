# coding: utf-8

"""
    Tator REST API

    Interface to the Tator backend.  # noqa: E501

    The version of the OpenAPI document: v1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ..configuration import Configuration


class AlgorithmLaunchSpec(object):
    """
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'algorithm_name': 'str',
        'media_ids': 'list[int]',
        'media_query': 'str'
    }

    attribute_map = {
        'algorithm_name': 'algorithm_name',
        'media_ids': 'media_ids',
        'media_query': 'media_query'
    }

    def __init__(self, algorithm_name=None, media_ids=None, media_query=None, local_vars_configuration=None):  # noqa: E501
        """AlgorithmLaunchSpec - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._algorithm_name = None
        self._media_ids = None
        self._media_query = None
        self.discriminator = None

        self.algorithm_name = algorithm_name
        if media_ids is not None:
            self.media_ids = media_ids
        if media_query is not None:
            self.media_query = media_query

    @property
    def algorithm_name(self):
        """
        Name of the algorithm to execute.

        :return: The algorithm_name of this AlgorithmLaunchSpec. 
        :rtype: str
        """
        return self._algorithm_name

    @algorithm_name.setter
    def algorithm_name(self, algorithm_name):
        """
        Name of the algorithm to execute.

        :param algorithm_name: The algorithm_name of this AlgorithmLaunchSpec.
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and algorithm_name is None:  # noqa: E501
            raise ValueError("Invalid value for `algorithm_name`, must not be `None`")  # noqa: E501

        self._algorithm_name = algorithm_name

    @property
    def media_ids(self):
        """
        List of media IDs. Must supply media_query or media_ids.

        :return: The media_ids of this AlgorithmLaunchSpec. 
        :rtype: list[int]
        """
        return self._media_ids

    @media_ids.setter
    def media_ids(self, media_ids):
        """
        List of media IDs. Must supply media_query or media_ids.

        :param media_ids: The media_ids of this AlgorithmLaunchSpec.
        :type: list[int]
        """

        self._media_ids = media_ids

    @property
    def media_query(self):
        """
        Query string used to filter media IDs. If supplied, media_ids will be ignored.

        :return: The media_query of this AlgorithmLaunchSpec. 
        :rtype: str
        """
        return self._media_query

    @media_query.setter
    def media_query(self, media_query):
        """
        Query string used to filter media IDs. If supplied, media_ids will be ignored.

        :param media_query: The media_query of this AlgorithmLaunchSpec.
        :type: str
        """

        self._media_query = media_query

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
        if not isinstance(other, AlgorithmLaunchSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AlgorithmLaunchSpec):
            return True

        return self.to_dict() != other.to_dict()
