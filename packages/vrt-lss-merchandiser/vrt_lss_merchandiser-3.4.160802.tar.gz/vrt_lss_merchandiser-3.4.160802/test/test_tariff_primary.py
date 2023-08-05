# coding: utf-8

"""
    VeeRoute.LSS Merchandiser

    VeeRoute.LSS Merchandiser API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_merchandiser
from vrt_lss_merchandiser.models.tariff_primary import TariffPrimary  # noqa: E501
from vrt_lss_merchandiser.rest import ApiException

class TestTariffPrimary(unittest.TestCase):
    """TariffPrimary unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TariffPrimary
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_merchandiser.models.tariff_primary.TariffPrimary()  # noqa: E501
        if include_optional :
            return TariffPrimary(
                cost_per_shift = 1000, 
                cost_per_meter = 0.1, 
                max_length = 200000, 
                cost_per_minute = 0.2, 
                max_time = 480
            )
        else :
            return TariffPrimary(
                cost_per_shift = 1000,
                cost_per_meter = 0.1,
                max_length = 200000,
                cost_per_minute = 0.2,
                max_time = 480,
        )

    def testTariffPrimary(self):
        """Test TariffPrimary"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
