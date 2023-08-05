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
from vrt_lss_clustering.models.cluster_settings import ClusterSettings  # noqa: E501
from vrt_lss_clustering.rest import ApiException

class TestClusterSettings(unittest.TestCase):
    """ClusterSettings unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ClusterSettings
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_clustering.models.cluster_settings.ClusterSettings()  # noqa: E501
        if include_optional :
            return ClusterSettings(
                configuration = 'default', 
                calculation_time = 30, 
                result_ttl = 10, 
                transport_factor = [
                    vrt_lss_clustering.models.transport_factor.TransportFactor(
                        transport_type = 'CAR', 
                        speed = 2.5, )
                    ], 
                routing = [
                    vrt_lss_clustering.models.routing.Routing(
                        transport_type = 'CAR', 
                        matrix = {"waypoints":[{"latitude":59.9345,"longitude":30.1504},{"latitude":59.942383,"longitude":30.258951},{"latitude":59.9545,"longitude":30.2004},{"latitude":59.89527,"longitude":30.261747},{"latitude":59.9745,"longitude":30.5004}],"distances":[[0,5822,1820,14130,23304],[5936,0,4931,8365,17731],[1819,4853,0,13161,22335],[14859,9056,13854,0,21440],[21777,16306,20772,19290,0]],"durations":[[0,13,7,24,36],[13,0,9,13,25],[7,9,0,21,32],[26,14,22,0,30],[34,23,30,28,0]]}, 
                        traffic_jams = [
                            vrt_lss_clustering.models.traffic_factor.TrafficFactor(
                                time_window = vrt_lss_clustering.models.time_window.TimeWindow(
                                    from = '2020-10-21T09:30+03:00', 
                                    to = '2020-10-21T19:45Z', ), 
                                length_multiplier = 2, 
                                length_additive = 20, 
                                time_multiplier = 2, 
                                time_additive = 30, )
                            ], )
                    ], 
                assumptions = vrt_lss_clustering.models.cluster_assumptions.ClusterAssumptions(
                    traffic_jams = False, 
                    flight_distance = True, ), 
                precision = 2, 
                limits = vrt_lss_clustering.models.cluster_limits.ClusterLimits(
                    min_points = 3, 
                    max_points = 3, )
            )
        else :
            return ClusterSettings(
        )

    def testClusterSettings(self):
        """Test ClusterSettings"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
