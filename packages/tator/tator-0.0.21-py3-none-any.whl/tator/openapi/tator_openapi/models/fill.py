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


class Fill(object):
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
        'color': 'object',
        'style': 'str'
    }

    attribute_map = {
        'color': 'color',
        'style': 'style'
    }

    def __init__(self, color=None, style=None, local_vars_configuration=None):  # noqa: E501
        """Fill - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._color = None
        self._style = None
        self.discriminator = None

        if color is not None:
            self.color = color
        if style is not None:
            self.style = style

    @property
    def color(self):
        """
        RGB array, RGBA array, or hex string.

        :return: The color of this Fill. 
        :rtype: object
        """
        return self._color

    @color.setter
    def color(self, color):
        """
        RGB array, RGBA array, or hex string.

        :param color: The color of this Fill.
        :type: object
        """

        self._color = color

    @property
    def style(self):
        """
        Type of fill effect

        :return: The style of this Fill. 
        :rtype: str
        """
        return self._style

    @style.setter
    def style(self, style):
        """
        Type of fill effect

        :param style: The style of this Fill.
        :type: str
        """
        allowed_values = ["fill", "blur", "gray"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and style not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `style` ({0}), must be one of {1}"  # noqa: E501
                .format(style, allowed_values)
            )

        self._style = style

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
        if not isinstance(other, Fill):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Fill):
            return True

        return self.to_dict() != other.to_dict()
