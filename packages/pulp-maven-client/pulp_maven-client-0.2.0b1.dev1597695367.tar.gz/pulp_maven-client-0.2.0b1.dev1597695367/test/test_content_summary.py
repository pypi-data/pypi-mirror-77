# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_maven
from pulpcore.client.pulp_maven.models.content_summary import ContentSummary  # noqa: E501
from pulpcore.client.pulp_maven.rest import ApiException

class TestContentSummary(unittest.TestCase):
    """ContentSummary unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ContentSummary
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_maven.models.content_summary.ContentSummary()  # noqa: E501
        if include_optional :
            return ContentSummary(
                added = None, 
                removed = None, 
                present = None
            )
        else :
            return ContentSummary(
                added = None,
                removed = None,
                present = None,
        )

    def testContentSummary(self):
        """Test ContentSummary"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
