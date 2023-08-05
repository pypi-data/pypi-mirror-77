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


class LocalizationTypeUpdate(object):
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
        'color_map': 'ColorMap',
        'description': 'str',
        'line_width': 'int',
        'name': 'str',
        'visible': 'bool'
    }

    attribute_map = {
        'color_map': 'colorMap',
        'description': 'description',
        'line_width': 'line_width',
        'name': 'name',
        'visible': 'visible'
    }

    def __init__(self, color_map=None, description=None, line_width=None, name=None, visible=True, local_vars_configuration=None):  # noqa: E501
        """LocalizationTypeUpdate - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._color_map = None
        self._description = None
        self._line_width = None
        self._name = None
        self._visible = None
        self.discriminator = None

        if color_map is not None:
            self.color_map = color_map
        if description is not None:
            self.description = description
        if line_width is not None:
            self.line_width = line_width
        if name is not None:
            self.name = name
        if visible is not None:
            self.visible = visible

    @property
    def color_map(self):
        """

        :return: The color_map of this LocalizationTypeUpdate. 
        :rtype: ColorMap
        """
        return self._color_map

    @color_map.setter
    def color_map(self, color_map):
        """

        :param color_map: The color_map of this LocalizationTypeUpdate.
        :type: ColorMap
        """

        self._color_map = color_map

    @property
    def description(self):
        """
        Description of the localization type.

        :return: The description of this LocalizationTypeUpdate. 
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Description of the localization type.

        :param description: The description of this LocalizationTypeUpdate.
        :type: str
        """

        self._description = description

    @property
    def line_width(self):
        """
        Width of the line used to draw the localization.

        :return: The line_width of this LocalizationTypeUpdate. 
        :rtype: int
        """
        return self._line_width

    @line_width.setter
    def line_width(self, line_width):
        """
        Width of the line used to draw the localization.

        :param line_width: The line_width of this LocalizationTypeUpdate.
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                line_width is not None and line_width < 1):  # noqa: E501
            raise ValueError("Invalid value for `line_width`, must be a value greater than or equal to `1`")  # noqa: E501

        self._line_width = line_width

    @property
    def name(self):
        """
        Name of the localization type.

        :return: The name of this LocalizationTypeUpdate. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Name of the localization type.

        :param name: The name of this LocalizationTypeUpdate.
        :type: str
        """

        self._name = name

    @property
    def visible(self):
        """
        Whether this type should be displayed in the UI.

        :return: The visible of this LocalizationTypeUpdate. 
        :rtype: bool
        """
        return self._visible

    @visible.setter
    def visible(self, visible):
        """
        Whether this type should be displayed in the UI.

        :param visible: The visible of this LocalizationTypeUpdate.
        :type: bool
        """

        self._visible = visible

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
        if not isinstance(other, LocalizationTypeUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LocalizationTypeUpdate):
            return True

        return self.to_dict() != other.to_dict()
