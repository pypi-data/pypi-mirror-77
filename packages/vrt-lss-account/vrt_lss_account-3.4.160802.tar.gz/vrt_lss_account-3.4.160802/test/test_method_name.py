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
from vrt_lss_account.models.method_name import MethodName  # noqa: E501
from vrt_lss_account.rest import ApiException

class TestMethodName(unittest.TestCase):
    """MethodName unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test MethodName
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_account.models.method_name.MethodName()  # noqa: E501
        if include_optional :
            return MethodName(
            )
        else :
            return MethodName(
        )

    def testMethodName(self):
        """Test MethodName"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
