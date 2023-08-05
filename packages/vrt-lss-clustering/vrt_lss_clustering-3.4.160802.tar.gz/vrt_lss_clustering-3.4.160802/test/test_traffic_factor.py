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
from vrt_lss_clustering.models.traffic_factor import TrafficFactor  # noqa: E501
from vrt_lss_clustering.rest import ApiException

class TestTrafficFactor(unittest.TestCase):
    """TrafficFactor unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TrafficFactor
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_clustering.models.traffic_factor.TrafficFactor()  # noqa: E501
        if include_optional :
            return TrafficFactor(
                time_window = vrt_lss_clustering.models.time_window.TimeWindow(
                    from = '2020-10-21T09:30+03:00', 
                    to = '2020-10-21T19:45Z', ), 
                length_multiplier = 2, 
                length_additive = 20, 
                time_multiplier = 2, 
                time_additive = 30
            )
        else :
            return TrafficFactor(
                time_window = vrt_lss_clustering.models.time_window.TimeWindow(
                    from = '2020-10-21T09:30+03:00', 
                    to = '2020-10-21T19:45Z', ),
        )

    def testTrafficFactor(self):
        """Test TrafficFactor"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
