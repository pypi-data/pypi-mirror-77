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
from vrt_ud.models.payment_details import PaymentDetails  # noqa: E501
from vrt_ud.rest import ApiException

class TestPaymentDetails(unittest.TestCase):
    """PaymentDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PaymentDetails
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_ud.models.payment_details.PaymentDetails()  # noqa: E501
        if include_optional :
            return PaymentDetails(
                bill_number_in_shift = '1', 
                bill_date_time = 'default', 
                customer_email = 'customer@company.com', 
                bill_amount_total = 1000, 
                fd_number = 'default', 
                fn_number = 'default', 
                qr_code = 'default', 
                payment_type = 'default', 
                approval_code = 'default', 
                kkt_registration_number = 'default', 
                invoice = 'default', 
                f_mark = 'default', 
                f_shift = 'default', 
                handmade_prepayment = 1000, 
                merchandise_lines = [
                    vrt_ud.models.merchandise_line.MerchandiseLine(
                        goods_name = 'boxes', 
                        goods_unit_name = 'box', 
                        goods_unit_price = 500, 
                        goods_amount = 2, 
                        goods_value = 1000, 
                        vat_rate = 'VAT0000', 
                        barcode = 'default', 
                        fact_time = '2020-10-21T09:30+03:00', )
                    ]
            )
        else :
            return PaymentDetails(
                bill_date_time = 'default',
                merchandise_lines = [
                    vrt_ud.models.merchandise_line.MerchandiseLine(
                        goods_name = 'boxes', 
                        goods_unit_name = 'box', 
                        goods_unit_price = 500, 
                        goods_amount = 2, 
                        goods_value = 1000, 
                        vat_rate = 'VAT0000', 
                        barcode = 'default', 
                        fact_time = '2020-10-21T09:30+03:00', )
                    ],
        )

    def testPaymentDetails(self):
        """Test PaymentDetails"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
