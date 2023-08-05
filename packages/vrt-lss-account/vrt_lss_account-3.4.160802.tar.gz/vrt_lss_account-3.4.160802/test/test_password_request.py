# coding: utf-8

"""
    VeeRoute.LSS Account

    LSS Account Panel  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_account
from vrt_lss_account.models.password_request import PasswordRequest  # noqa: E501
from vrt_lss_account.rest import ApiException

class TestPasswordRequest(unittest.TestCase):
    """PasswordRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PasswordRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_account.models.password_request.PasswordRequest()  # noqa: E501
        if include_optional :
            return PasswordRequest(
                current_password = 'password', 
                new_password = 'password'
            )
        else :
            return PasswordRequest(
                current_password = 'password',
                new_password = 'password',
        )

    def testPasswordRequest(self):
        """Test PasswordRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
