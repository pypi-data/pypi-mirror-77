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

import vrt_lss_clustering
from vrt_lss_clustering.api.validate_api import ValidateApi  # noqa: E501
from vrt_lss_clustering.rest import ApiException


class TestValidateApi(unittest.TestCase):
    """ValidateApi unit test stubs"""

    def setUp(self):
        self.api = vrt_lss_clustering.api.validate_api.ValidateApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_validate(self):
        """Test case for validate

        Data validation for clustering.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
