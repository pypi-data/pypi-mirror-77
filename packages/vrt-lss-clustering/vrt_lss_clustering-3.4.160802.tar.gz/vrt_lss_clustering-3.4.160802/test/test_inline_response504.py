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
from vrt_lss_clustering.models.inline_response504 import InlineResponse504  # noqa: E501
from vrt_lss_clustering.rest import ApiException

class TestInlineResponse504(unittest.TestCase):
    """InlineResponse504 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse504
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_clustering.models.inline_response504.InlineResponse504()  # noqa: E501
        if include_optional :
            return InlineResponse504(
                tracedata = vrt_lss_clustering.models.trace_data.TraceData(
                    code = 'client_server_service_time_id', ), 
                message = 'Gateway Timeout', 
                code = 1504
            )
        else :
            return InlineResponse504(
                code = 1504,
        )

    def testInlineResponse504(self):
        """Test InlineResponse504"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
