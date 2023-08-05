# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_ansible.configuration import Configuration


class AnsibleRoleResponse(object):
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
        'artifact': 'str',
        'pulp_href': 'str',
        'pulp_created': 'datetime',
        'version': 'str',
        'name': 'str',
        'namespace': 'str'
    }

    attribute_map = {
        'artifact': 'artifact',
        'pulp_href': 'pulp_href',
        'pulp_created': 'pulp_created',
        'version': 'version',
        'name': 'name',
        'namespace': 'namespace'
    }

    def __init__(self, artifact=None, pulp_href=None, pulp_created=None, version=None, name=None, namespace=None, local_vars_configuration=None):  # noqa: E501
        """AnsibleRoleResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._artifact = None
        self._pulp_href = None
        self._pulp_created = None
        self._version = None
        self._name = None
        self._namespace = None
        self.discriminator = None

        self.artifact = artifact
        if pulp_href is not None:
            self.pulp_href = pulp_href
        if pulp_created is not None:
            self.pulp_created = pulp_created
        self.version = version
        self.name = name
        self.namespace = namespace

    @property
    def artifact(self):
        """Gets the artifact of this AnsibleRoleResponse.  # noqa: E501

        Artifact file representing the physical content  # noqa: E501

        :return: The artifact of this AnsibleRoleResponse.  # noqa: E501
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """Sets the artifact of this AnsibleRoleResponse.

        Artifact file representing the physical content  # noqa: E501

        :param artifact: The artifact of this AnsibleRoleResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and artifact is None:  # noqa: E501
            raise ValueError("Invalid value for `artifact`, must not be `None`")  # noqa: E501

        self._artifact = artifact

    @property
    def pulp_href(self):
        """Gets the pulp_href of this AnsibleRoleResponse.  # noqa: E501


        :return: The pulp_href of this AnsibleRoleResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this AnsibleRoleResponse.


        :param pulp_href: The pulp_href of this AnsibleRoleResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def pulp_created(self):
        """Gets the pulp_created of this AnsibleRoleResponse.  # noqa: E501

        Timestamp of creation.  # noqa: E501

        :return: The pulp_created of this AnsibleRoleResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._pulp_created

    @pulp_created.setter
    def pulp_created(self, pulp_created):
        """Sets the pulp_created of this AnsibleRoleResponse.

        Timestamp of creation.  # noqa: E501

        :param pulp_created: The pulp_created of this AnsibleRoleResponse.  # noqa: E501
        :type: datetime
        """

        self._pulp_created = pulp_created

    @property
    def version(self):
        """Gets the version of this AnsibleRoleResponse.  # noqa: E501


        :return: The version of this AnsibleRoleResponse.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this AnsibleRoleResponse.


        :param version: The version of this AnsibleRoleResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def name(self):
        """Gets the name of this AnsibleRoleResponse.  # noqa: E501


        :return: The name of this AnsibleRoleResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AnsibleRoleResponse.


        :param name: The name of this AnsibleRoleResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def namespace(self):
        """Gets the namespace of this AnsibleRoleResponse.  # noqa: E501


        :return: The namespace of this AnsibleRoleResponse.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this AnsibleRoleResponse.


        :param namespace: The namespace of this AnsibleRoleResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and namespace is None:  # noqa: E501
            raise ValueError("Invalid value for `namespace`, must not be `None`")  # noqa: E501

        self._namespace = namespace

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
        if not isinstance(other, AnsibleRoleResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AnsibleRoleResponse):
            return True

        return self.to_dict() != other.to_dict()
