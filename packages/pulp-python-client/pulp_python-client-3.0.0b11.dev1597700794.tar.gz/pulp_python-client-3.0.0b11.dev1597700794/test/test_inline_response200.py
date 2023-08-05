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

import pulpcore.client.pulp_python
from pulpcore.client.pulp_python.models.inline_response200 import InlineResponse200  # noqa: E501
from pulpcore.client.pulp_python.rest import ApiException

class TestInlineResponse200(unittest.TestCase):
    """InlineResponse200 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse200
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_python.models.inline_response200.InlineResponse200()  # noqa: E501
        if include_optional :
            return InlineResponse200(
                count = 123, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulp_python.models.python/python_package_content_response.python.PythonPackageContentResponse(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        artifact = '0', 
                        filename = '0', 
                        packagetype = '0', 
                        name = '0', 
                        version = '0', 
                        metadata_version = '0', 
                        summary = '0', 
                        description = '0', 
                        keywords = '0', 
                        home_page = '0', 
                        download_url = '0', 
                        author = '0', 
                        author_email = '0', 
                        maintainer = '0', 
                        maintainer_email = '0', 
                        license = '0', 
                        requires_python = '0', 
                        project_url = '0', 
                        platform = '0', 
                        supported_platform = '0', 
                        requires_dist = pulpcore.client.pulp_python.models.requires_dist.requires_dist(), 
                        provides_dist = pulpcore.client.pulp_python.models.provides_dist.provides_dist(), 
                        obsoletes_dist = pulpcore.client.pulp_python.models.obsoletes_dist.obsoletes_dist(), 
                        requires_external = pulpcore.client.pulp_python.models.requires_external.requires_external(), 
                        classifiers = pulpcore.client.pulp_python.models.classifiers.classifiers(), )
                    ]
            )
        else :
            return InlineResponse200(
        )

    def testInlineResponse200(self):
        """Test InlineResponse200"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
