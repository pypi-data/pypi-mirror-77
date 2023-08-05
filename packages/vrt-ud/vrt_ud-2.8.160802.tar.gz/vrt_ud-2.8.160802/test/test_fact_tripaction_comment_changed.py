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
from vrt_ud.models.fact_tripaction_comment_changed import FactTripactionCommentChanged  # noqa: E501
from vrt_ud.rest import ApiException

class TestFactTripactionCommentChanged(unittest.TestCase):
    """FactTripactionCommentChanged unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test FactTripactionCommentChanged
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_ud.models.fact_tripaction_comment_changed.FactTripactionCommentChanged()  # noqa: E501
        if include_optional :
            return FactTripactionCommentChanged(
                performer_id = 'f_887', 
                trip_id = 'default', 
                order_id = 'default', 
                demand_key = 'default', 
                old_comment_value = 'default', 
                new_comment_value = 'default', 
                fact_time = '2020-10-21T09:30+03:00'
            )
        else :
            return FactTripactionCommentChanged(
                performer_id = 'f_887',
                trip_id = 'default',
                order_id = 'default',
                demand_key = 'default',
                old_comment_value = 'default',
                new_comment_value = 'default',
        )

    def testFactTripactionCommentChanged(self):
        """Test FactTripactionCommentChanged"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
