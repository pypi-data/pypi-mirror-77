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


class User(object):
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
        'member_of': 'list[UserIdentity]',
        'id': 'str',
        'external_id': 'str',
        'enabled': 'bool',
        'first_name': 'str',
        'last_name': 'str',
        'email': 'str',
        'provider': 'str',
        'roles': 'Roles',
        'org_id': 'str',
        'type': 'str',
        'created': 'datetime',
        'updated': 'datetime',
        'auto_created': 'bool',
        'upstream_user_identities': 'list[UpstreamUserIdentity]'
    }

    attribute_map = {
        'member_of': 'member_of',
        'id': 'id',
        'external_id': 'external_id',
        'enabled': 'enabled',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
        'provider': 'provider',
        'roles': 'roles',
        'org_id': 'org_id',
        'type': 'type',
        'created': 'created',
        'updated': 'updated',
        'auto_created': 'auto_created',
        'upstream_user_identities': 'upstream_user_identities'
    }

    def __init__(self, member_of=None, id=None, external_id=None, enabled=None, first_name=None, last_name=None, email=None, provider=None, roles=None, org_id=None, type=None, created=None, updated=None, auto_created=False, upstream_user_identities=None, local_vars_configuration=None):  # noqa: E501
        """User - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._member_of = None
        self._id = None
        self._external_id = None
        self._enabled = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._provider = None
        self._roles = None
        self._org_id = None
        self._type = None
        self._created = None
        self._updated = None
        self._auto_created = None
        self._upstream_user_identities = None
        self.discriminator = None

        if member_of is not None:
            self.member_of = member_of
        if id is not None:
            self.id = id
        if external_id is not None:
            self.external_id = external_id
        if enabled is not None:
            self.enabled = enabled
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email
        self.provider = provider
        if roles is not None:
            self.roles = roles
        if org_id is not None:
            self.org_id = org_id
        if type is not None:
            self.type = type
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated
        if auto_created is not None:
            self.auto_created = auto_created
        if upstream_user_identities is not None:
            self.upstream_user_identities = upstream_user_identities

    @property
    def member_of(self):
        """Gets the member_of of this User.  # noqa: E501

        List of groups that the user is a member of  # noqa: E501

        :return: The member_of of this User.  # noqa: E501
        :rtype: list[UserIdentity]
        """
        return self._member_of

    @member_of.setter
    def member_of(self, member_of):
        """Sets the member_of of this User.

        List of groups that the user is a member of  # noqa: E501

        :param member_of: The member_of of this User.  # noqa: E501
        :type: list[UserIdentity]
        """

        self._member_of = member_of

    @property
    def id(self):
        """Gets the id of this User.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The id of this User.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this User.

        Unique identifier  # noqa: E501

        :param id: The id of this User.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def external_id(self):
        """Gets the external_id of this User.  # noqa: E501

        External unique identifier  # noqa: E501

        :return: The external_id of this User.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this User.

        External unique identifier  # noqa: E501

        :param external_id: The external_id of this User.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                external_id is not None and len(external_id) > 100):
            raise ValueError("Invalid value for `external_id`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                external_id is not None and len(external_id) < 1):
            raise ValueError("Invalid value for `external_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._external_id = external_id

    @property
    def enabled(self):
        """Gets the enabled of this User.  # noqa: E501

        Enable/Disable a user  # noqa: E501

        :return: The enabled of this User.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this User.

        Enable/Disable a user  # noqa: E501

        :param enabled: The enabled of this User.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def first_name(self):
        """Gets the first_name of this User.  # noqa: E501

        User's first name  # noqa: E501

        :return: The first_name of this User.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this User.

        User's first name  # noqa: E501

        :param first_name: The first_name of this User.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                first_name is not None and len(first_name) > 100):
            raise ValueError("Invalid value for `first_name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                first_name is not None and len(first_name) < 1):
            raise ValueError("Invalid value for `first_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this User.  # noqa: E501

        User's last name  # noqa: E501

        :return: The last_name of this User.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this User.

        User's last name  # noqa: E501

        :param last_name: The last_name of this User.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                last_name is not None and len(last_name) > 100):
            raise ValueError("Invalid value for `last_name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                last_name is not None and len(last_name) < 0):
            raise ValueError("Invalid value for `last_name`, length must be greater than or equal to `0`")  # noqa: E501

        self._last_name = last_name

    @property
    def email(self):
        """Gets the email of this User.  # noqa: E501

        User's email address  # noqa: E501

        :return: The email of this User.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this User.

        User's email address  # noqa: E501

        :param email: The email of this User.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) > 100):
            raise ValueError("Invalid value for `email`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) < 0):
            raise ValueError("Invalid value for `email`, length must be greater than or equal to `0`")  # noqa: E501

        self._email = email

    @property
    def provider(self):
        """Gets the provider of this User.  # noqa: E501

        Upstream IdP name  # noqa: E501

        :return: The provider of this User.  # noqa: E501
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """Sets the provider of this User.

        Upstream IdP name  # noqa: E501

        :param provider: The provider of this User.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                provider is not None and len(provider) > 100):
            raise ValueError("Invalid value for `provider`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                provider is not None and len(provider) < 1):
            raise ValueError("Invalid value for `provider`, length must be greater than or equal to `1`")  # noqa: E501

        self._provider = provider

    @property
    def roles(self):
        """Gets the roles of this User.  # noqa: E501


        :return: The roles of this User.  # noqa: E501
        :rtype: Roles
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this User.


        :param roles: The roles of this User.  # noqa: E501
        :type: Roles
        """

        self._roles = roles

    @property
    def org_id(self):
        """Gets the org_id of this User.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The org_id of this User.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this User.

        Unique identifier  # noqa: E501

        :param org_id: The org_id of this User.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def type(self):
        """Gets the type of this User.  # noqa: E501

        Type of user  # noqa: E501

        :return: The type of this User.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this User.

        Type of user  # noqa: E501

        :param type: The type of this User.  # noqa: E501
        :type: str
        """
        allowed_values = ["user", "group", "sysgroup", "bigroup"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def created(self):
        """Gets the created of this User.  # noqa: E501

        Creation time  # noqa: E501

        :return: The created of this User.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this User.

        Creation time  # noqa: E501

        :param created: The created of this User.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this User.  # noqa: E501

        Update time  # noqa: E501

        :return: The updated of this User.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this User.

        Update time  # noqa: E501

        :param updated: The updated of this User.  # noqa: E501
        :type: datetime
        """

        self._updated = updated

    @property
    def auto_created(self):
        """Gets the auto_created of this User.  # noqa: E501

        Whether the user was automatically created as part of another process such as logging in. On creation, this flag being true serves to trigger any behaviour tied to automatically created users, such as addition to special groups. On read, it can serve to indicate whether the user was automatically created. On update it will ensure that the automatically triggered behaviour still holds true.   # noqa: E501

        :return: The auto_created of this User.  # noqa: E501
        :rtype: bool
        """
        return self._auto_created

    @auto_created.setter
    def auto_created(self, auto_created):
        """Sets the auto_created of this User.

        Whether the user was automatically created as part of another process such as logging in. On creation, this flag being true serves to trigger any behaviour tied to automatically created users, such as addition to special groups. On read, it can serve to indicate whether the user was automatically created. On update it will ensure that the automatically triggered behaviour still holds true.   # noqa: E501

        :param auto_created: The auto_created of this User.  # noqa: E501
        :type: bool
        """

        self._auto_created = auto_created

    @property
    def upstream_user_identities(self):
        """Gets the upstream_user_identities of this User.  # noqa: E501

        The upstream identities this user can use to log in to the system. When a user logs in, their identity in this system will be determined by matching against this list. Note that this implies that entries in this list are globally unique.   # noqa: E501

        :return: The upstream_user_identities of this User.  # noqa: E501
        :rtype: list[UpstreamUserIdentity]
        """
        return self._upstream_user_identities

    @upstream_user_identities.setter
    def upstream_user_identities(self, upstream_user_identities):
        """Sets the upstream_user_identities of this User.

        The upstream identities this user can use to log in to the system. When a user logs in, their identity in this system will be determined by matching against this list. Note that this implies that entries in this list are globally unique.   # noqa: E501

        :param upstream_user_identities: The upstream_user_identities of this User.  # noqa: E501
        :type: list[UpstreamUserIdentity]
        """

        self._upstream_user_identities = upstream_user_identities

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
        if not isinstance(other, User):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, User):
            return True

        return self.to_dict() != other.to_dict()
