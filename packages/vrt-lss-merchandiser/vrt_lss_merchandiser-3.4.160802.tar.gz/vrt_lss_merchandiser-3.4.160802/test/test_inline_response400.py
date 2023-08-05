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
from vrt_lss_merchandiser.models.inline_response400 import InlineResponse400  # noqa: E501
from vrt_lss_merchandiser.rest import ApiException

class TestInlineResponse400(unittest.TestCase):
    """InlineResponse400 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse400
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_merchandiser.models.inline_response400.InlineResponse400()  # noqa: E501
        if include_optional :
            return InlineResponse400(
                tracedata = vrt_lss_merchandiser.models.trace_data.TraceData(
                    code = 'client_server_service_time_id', ), 
                message = 'Bad Request', 
                code = 1400, 
                validations = [
                    vrt_lss_merchandiser.models.validation.Validation(
                        type = 'info', 
                        entity_key = 'ord0001', 
                        entity_type = 'order', 
                        info = 'bad time windows', )
                    ]
            )
        else :
            return InlineResponse400(
                code = 1400,
        )

    def testInlineResponse400(self):
        """Test InlineResponse400"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
