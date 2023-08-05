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


class Membership(object):
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
        'id': 'int',
        'permission': 'str',
        'username': 'str'
    }

    attribute_map = {
        'id': 'id',
        'permission': 'permission',
        'username': 'username'
    }

    def __init__(self, id=None, permission=None, username=None, local_vars_configuration=None):  # noqa: E501
        """Membership - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._permission = None
        self._username = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if permission is not None:
            self.permission = permission
        if username is not None:
            self.username = username

    @property
    def id(self):
        """
        Unique integer identifying a membership.

        :return: The id of this Membership. 
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Unique integer identifying a membership.

        :param id: The id of this Membership.
        :type: int
        """

        self._id = id

    @property
    def permission(self):
        """
        User permission level for the project.

        :return: The permission of this Membership. 
        :rtype: str
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """
        User permission level for the project.

        :param permission: The permission of this Membership.
        :type: str
        """
        allowed_values = ["view_only", "can_edit", "can_transfer", "can_execute", "full_control"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and permission not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `permission` ({0}), must be one of {1}"  # noqa: E501
                .format(permission, allowed_values)
            )

        self._permission = permission

    @property
    def username(self):
        """
        Username for the membership.

        :return: The username of this Membership. 
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Username for the membership.

        :param username: The username of this Membership.
        :type: str
        """

        self._username = username

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
        if not isinstance(other, Membership):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Membership):
            return True

        return self.to_dict() != other.to_dict()
