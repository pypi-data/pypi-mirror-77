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


class Project(object):
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
        'name': 'str',
        'num_files': 'int',
        'permission': 'str',
        'size': 'int',
        'summary': 'str',
        'thumb': 'str',
        'usernames': 'list[str]'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'num_files': 'num_files',
        'permission': 'permission',
        'size': 'size',
        'summary': 'summary',
        'thumb': 'thumb',
        'usernames': 'usernames'
    }

    def __init__(self, id=None, name=None, num_files=None, permission=None, size=None, summary='', thumb=None, usernames=None, local_vars_configuration=None):  # noqa: E501
        """Project - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._num_files = None
        self._permission = None
        self._size = None
        self._summary = None
        self._thumb = None
        self._usernames = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if num_files is not None:
            self.num_files = num_files
        if permission is not None:
            self.permission = permission
        if size is not None:
            self.size = size
        if summary is not None:
            self.summary = summary
        if thumb is not None:
            self.thumb = thumb
        if usernames is not None:
            self.usernames = usernames

    @property
    def id(self):
        """
        Unique integer identifying the project.

        :return: The id of this Project. 
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Unique integer identifying the project.

        :param id: The id of this Project.
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """
        Name of the project.

        :return: The name of this Project. 
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Name of the project.

        :param name: The name of this Project.
        :type: str
        """

        self._name = name

    @property
    def num_files(self):
        """
        Number of files in the project.

        :return: The num_files of this Project. 
        :rtype: int
        """
        return self._num_files

    @num_files.setter
    def num_files(self, num_files):
        """
        Number of files in the project.

        :param num_files: The num_files of this Project.
        :type: int
        """

        self._num_files = num_files

    @property
    def permission(self):
        """
        Permission level of user making request.

        :return: The permission of this Project. 
        :rtype: str
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """
        Permission level of user making request.

        :param permission: The permission of this Project.
        :type: str
        """

        self._permission = permission

    @property
    def size(self):
        """
        Size of the project in bytes.

        :return: The size of this Project. 
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Size of the project in bytes.

        :param size: The size of this Project.
        :type: int
        """

        self._size = size

    @property
    def summary(self):
        """
        Summary of the project.

        :return: The summary of this Project. 
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Summary of the project.

        :param summary: The summary of this Project.
        :type: str
        """

        self._summary = summary

    @property
    def thumb(self):
        """
        URL of thumbnail used to represent the project.

        :return: The thumb of this Project. 
        :rtype: str
        """
        return self._thumb

    @thumb.setter
    def thumb(self, thumb):
        """
        URL of thumbnail used to represent the project.

        :param thumb: The thumb of this Project.
        :type: str
        """

        self._thumb = thumb

    @property
    def usernames(self):
        """
        List of usernames of project members.

        :return: The usernames of this Project. 
        :rtype: list[str]
        """
        return self._usernames

    @usernames.setter
    def usernames(self, usernames):
        """
        List of usernames of project members.

        :param usernames: The usernames of this Project.
        :type: list[str]
        """

        self._usernames = usernames

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
        if not isinstance(other, Project):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Project):
            return True

        return self.to_dict() != other.to_dict()
