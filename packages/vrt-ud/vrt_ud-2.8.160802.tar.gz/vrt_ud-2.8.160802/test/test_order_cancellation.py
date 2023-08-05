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
from vrt_ud.models.order_cancellation import OrderCancellation  # noqa: E501
from vrt_ud.rest import ApiException

class TestOrderCancellation(unittest.TestCase):
    """OrderCancellation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OrderCancellation
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_ud.models.order_cancellation.OrderCancellation()  # noqa: E501
        if include_optional :
            return OrderCancellation(
                goods_name = 'boxes', 
                goods_amount = 2, 
                cancellation_reason = 'no reason', 
                fact_time = '2020-10-21T09:30+03:00'
            )
        else :
            return OrderCancellation(
                goods_name = 'boxes',
                goods_amount = 2,
                cancellation_reason = 'no reason',
        )

    def testOrderCancellation(self):
        """Test OrderCancellation"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
