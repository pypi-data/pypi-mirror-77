# coding: utf-8

"""
    VeeRoute.UD

    VeeRoute.UD API  # noqa: E501

    The version of the OpenAPI document: 2.8.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_ud
from vrt_ud.models.inline_response500 import InlineResponse500  # noqa: E501
from vrt_ud.rest import ApiException

class TestInlineResponse500(unittest.TestCase):
    """InlineResponse500 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse500
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_ud.models.inline_response500.InlineResponse500()  # noqa: E501
        if include_optional :
            return InlineResponse500(
                tracedata = vrt_ud.models.trace_data.TraceData(
                    code = 'client_server_service_time_id', ), 
                message = 'Internal Server Error', 
                code = 1500
            )
        else :
            return InlineResponse500(
                code = 1500,
        )

    def testInlineResponse500(self):
        """Test InlineResponse500"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
