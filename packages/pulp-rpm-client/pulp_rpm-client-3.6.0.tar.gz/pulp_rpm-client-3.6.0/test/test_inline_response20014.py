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

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.inline_response20014 import InlineResponse20014  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestInlineResponse20014(unittest.TestCase):
    """InlineResponse20014 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse20014
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.inline_response20014.InlineResponse20014()  # noqa: E501
        if include_optional :
            return InlineResponse20014(
                count = 123, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulp_rpm.models.repository_version_response.RepositoryVersionResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        number = 56, 
                        base_version = '0', 
                        content_summary = null, )
                    ]
            )
        else :
            return InlineResponse20014(
        )

    def testInlineResponse20014(self):
        """Test InlineResponse20014"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
