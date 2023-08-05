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


class InlineResponse500(object):
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
        'tracedata': 'TraceData',
        'message': 'str',
        'code': 'int'
    }

    attribute_map = {
        'tracedata': 'tracedata',
        'message': 'message',
        'code': 'code'
    }

    def __init__(self, tracedata=None, message=None, code=None, local_vars_configuration=None):  # noqa: E501
        """InlineResponse500 - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._tracedata = None
        self._message = None
        self._code = None
        self.discriminator = None

        if tracedata is not None:
            self.tracedata = tracedata
        if message is not None:
            self.message = message
        self.code = code

    @property
    def tracedata(self):
        """Gets the tracedata of this InlineResponse500.  # noqa: E501


        :return: The tracedata of this InlineResponse500.  # noqa: E501
        :rtype: TraceData
        """
        return self._tracedata

    @tracedata.setter
    def tracedata(self, tracedata):
        """Sets the tracedata of this InlineResponse500.


        :param tracedata: The tracedata of this InlineResponse500.  # noqa: E501
        :type: TraceData
        """

        self._tracedata = tracedata

    @property
    def message(self):
        """Gets the message of this InlineResponse500.  # noqa: E501

        Error message.  # noqa: E501

        :return: The message of this InlineResponse500.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this InlineResponse500.

        Error message.  # noqa: E501

        :param message: The message of this InlineResponse500.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def code(self):
        """Gets the code of this InlineResponse500.  # noqa: E501

        Error code.  # noqa: E501

        :return: The code of this InlineResponse500.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this InlineResponse500.

        Error code.  # noqa: E501

        :param code: The code of this InlineResponse500.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and code is None:  # noqa: E501
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and code > 10000):  # noqa: E501
            raise ValueError("Invalid value for `code`, must be a value less than or equal to `10000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                code is not None and code < 0):  # noqa: E501
            raise ValueError("Invalid value for `code`, must be a value greater than or equal to `0`")  # noqa: E501

        self._code = code

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
        if not isinstance(other, InlineResponse500):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse500):
            return True

        return self.to_dict() != other.to_dict()
