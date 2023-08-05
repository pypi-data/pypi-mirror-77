# coding: utf-8

"""
    VeeRoute.LSS Clustering

    VeeRoute.LSS Clustering API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_clustering
from vrt_lss_clustering.models.transport_type import TransportType  # noqa: E501
from vrt_lss_clustering.rest import ApiException

class TestTransportType(unittest.TestCase):
    """TransportType unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TransportType
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_clustering.models.transport_type.TransportType()  # noqa: E501
        if include_optional :
            return TransportType(
            )
        else :
            return TransportType(
        )

    def testTransportType(self):
        """Test TransportType"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
