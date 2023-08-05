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
from vrt_lss_account.models.additional_quota import AdditionalQuota  # noqa: E501
from vrt_lss_account.rest import ApiException

class TestAdditionalQuota(unittest.TestCase):
    """AdditionalQuota unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test AdditionalQuota
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_account.models.additional_quota.AdditionalQuota()  # noqa: E501
        if include_optional :
            return AdditionalQuota(
                date_window = vrt_lss_account.models.date_window.DateWindow(
                    from = 'Wed Oct 21 03:00:00 MSK 2020', 
                    to = 'Wed Oct 21 03:00:00 MSK 2020', ), 
                quota = vrt_lss_account.models.quota.Quota(
                    services = [
                        vrt_lss_account.models.service_quota.ServiceQuota(
                            service = 'Lastmile', 
                            methods = [
                                vrt_lss_account.models.method_quota.MethodQuota(
                                    method = 'plan', 
                                    points_per_request = 15, 
                                    points_per_day = 1500, 
                                    points_per_date_window = 1500, 
                                    max_concurrent_execution = 5, )
                                ], )
                        ], )
            )
        else :
            return AdditionalQuota(
                date_window = vrt_lss_account.models.date_window.DateWindow(
                    from = 'Wed Oct 21 03:00:00 MSK 2020', 
                    to = 'Wed Oct 21 03:00:00 MSK 2020', ),
                quota = vrt_lss_account.models.quota.Quota(
                    services = [
                        vrt_lss_account.models.service_quota.ServiceQuota(
                            service = 'Lastmile', 
                            methods = [
                                vrt_lss_account.models.method_quota.MethodQuota(
                                    method = 'plan', 
                                    points_per_request = 15, 
                                    points_per_day = 1500, 
                                    points_per_date_window = 1500, 
                                    max_concurrent_execution = 5, )
                                ], )
                        ], ),
        )

    def testAdditionalQuota(self):
        """Test AdditionalQuota"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
