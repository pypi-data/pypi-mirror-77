# coding: utf-8

"""
    VeeRoute.LSS Account

    LSS Account Panel  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from vrt_lss_account.configuration import Configuration


class TokenRequest(object):
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
        'username': 'str',
        'password': 'str',
        'ttl_seconds': 'int'
    }

    attribute_map = {
        'username': 'username',
        'password': 'password',
        'ttl_seconds': 'ttl_seconds'
    }

    def __init__(self, username=None, password=None, ttl_seconds=86400, local_vars_configuration=None):  # noqa: E501
        """TokenRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._username = None
        self._password = None
        self._ttl_seconds = None
        self.discriminator = None

        self.username = username
        self.password = password
        if ttl_seconds is not None:
            self.ttl_seconds = ttl_seconds

    @property
    def username(self):
        """Gets the username of this TokenRequest.  # noqa: E501

        Login.  # noqa: E501

        :return: The username of this TokenRequest.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this TokenRequest.

        Login.  # noqa: E501

        :param username: The username of this TokenRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and username is None:  # noqa: E501
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                username is not None and len(username) > 256):
            raise ValueError("Invalid value for `username`, length must be less than or equal to `256`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                username is not None and len(username) < 1):
            raise ValueError("Invalid value for `username`, length must be greater than or equal to `1`")  # noqa: E501

        self._username = username

    @property
    def password(self):
        """Gets the password of this TokenRequest.  # noqa: E501

        Password.  # noqa: E501

        :return: The password of this TokenRequest.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this TokenRequest.

        Password.  # noqa: E501

        :param password: The password of this TokenRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and password is None:  # noqa: E501
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                password is not None and len(password) > 1000):
            raise ValueError("Invalid value for `password`, length must be less than or equal to `1000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                password is not None and len(password) < 1):
            raise ValueError("Invalid value for `password`, length must be greater than or equal to `1`")  # noqa: E501

        self._password = password

    @property
    def ttl_seconds(self):
        """Gets the ttl_seconds of this TokenRequest.  # noqa: E501

        Token validity time, in seconds.  # noqa: E501

        :return: The ttl_seconds of this TokenRequest.  # noqa: E501
        :rtype: int
        """
        return self._ttl_seconds

    @ttl_seconds.setter
    def ttl_seconds(self, ttl_seconds):
        """Sets the ttl_seconds of this TokenRequest.

        Token validity time, in seconds.  # noqa: E501

        :param ttl_seconds: The ttl_seconds of this TokenRequest.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                ttl_seconds is not None and ttl_seconds > 31556926):  # noqa: E501
            raise ValueError("Invalid value for `ttl_seconds`, must be a value less than or equal to `31556926`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                ttl_seconds is not None and ttl_seconds < 60):  # noqa: E501
            raise ValueError("Invalid value for `ttl_seconds`, must be a value greater than or equal to `60`")  # noqa: E501

        self._ttl_seconds = ttl_seconds

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
        if not isinstance(other, TokenRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TokenRequest):
            return True

        return self.to_dict() != other.to_dict()
