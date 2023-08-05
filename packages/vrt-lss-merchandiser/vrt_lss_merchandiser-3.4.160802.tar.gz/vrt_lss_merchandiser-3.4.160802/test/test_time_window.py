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
from vrt_lss_merchandiser.models.time_window import TimeWindow  # noqa: E501
from vrt_lss_merchandiser.rest import ApiException

class TestTimeWindow(unittest.TestCase):
    """TimeWindow unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TimeWindow
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_merchandiser.models.time_window.TimeWindow()  # noqa: E501
        if include_optional :
            return TimeWindow(
                _from = '2020-10-21T09:30+03:00', 
                to = '2020-10-21T19:45Z'
            )
        else :
            return TimeWindow(
                _from = '2020-10-21T09:30+03:00',
                to = '2020-10-21T19:45Z',
        )

    def testTimeWindow(self):
        """Test TimeWindow"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
