# coding: utf-8

"""
    VeeRoute.LSS Delivery

    VeeRoute.LSS Delivery API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_delivery
from vrt_lss_delivery.models.transport_factor import TransportFactor  # noqa: E501
from vrt_lss_delivery.rest import ApiException

class TestTransportFactor(unittest.TestCase):
    """TransportFactor unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TransportFactor
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_delivery.models.transport_factor.TransportFactor()  # noqa: E501
        if include_optional :
            return TransportFactor(
                transport_type = 'CAR', 
                speed = 2.5
            )
        else :
            return TransportFactor(
                transport_type = 'CAR',
                speed = 2.5,
        )

    def testTransportFactor(self):
        """Test TransportFactor"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
