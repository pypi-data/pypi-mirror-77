# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.08.17
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import agilicus_api
from agilicus_api.models.audit import Audit  # noqa: E501
from agilicus_api.rest import ApiException

class TestAudit(unittest.TestCase):
    """Audit unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Audit
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.audit.Audit()  # noqa: E501
        if include_optional :
            return Audit(
                user_id = 'jjkkGmwB9oTJWDjIglTU', 
                target_resource_type = '/v1/groups', 
                api_name = 'urn:api:agilicus', 
                org_id = '2jkMGmwB9o7JW3jIglNZ', 
                time = '2019-05-16T19:11:18Z', 
                action = '0', 
                source_ip = '192.0.2.1', 
                target_id = '2jkdCmwB9u7Jh3KIglNZ', 
                token_id = 'XMYdZy7yAiudMDxQqgDwkY', 
                trace_id = '00b893c9ec7c0089c3da65e7c9e2263a', 
                session = '00b893c9ec7c0089c3da65e7c9e2263a'
            )
        else :
            return Audit(
        )

    def testAudit(self):
        """Test Audit"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
