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
from pulpcore.client.pulp_python.models.python_bander_remote import PythonBanderRemote  # noqa: E501
from pulpcore.client.pulp_python.rest import ApiException

class TestPythonBanderRemote(unittest.TestCase):
    """PythonBanderRemote unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PythonBanderRemote
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_python.models.python_bander_remote.PythonBanderRemote()  # noqa: E501
        if include_optional :
            return PythonBanderRemote(
                config = bytes(b'blah'), 
                name = '0'
            )
        else :
            return PythonBanderRemote(
                config = bytes(b'blah'),
                name = '0',
        )

    def testPythonBanderRemote(self):
        """Test PythonBanderRemote"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
