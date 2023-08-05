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
from agilicus_api.models.combined_rules import CombinedRules  # noqa: E501
from agilicus_api.rest import ApiException

class TestCombinedRules(unittest.TestCase):
    """CombinedRules unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CombinedRules
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.combined_rules.CombinedRules()  # noqa: E501
        if include_optional :
            return CombinedRules(
                status = agilicus_api.models.combined_rules_status.CombinedRulesStatus(
                    app_id = '123', 
                    org_id = '123', 
                    role_id = '123', 
                    role_name = '0', 
                    rules = [
                        agilicus_api.models.rule_v2.RuleV2(
                            metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                            spec = agilicus_api.models.rule_spec.RuleSpec(
                                comments = 'This rule allows access to all static content of the application for any user, even if they are not authenticated.', 
                                condition = agilicus_api.models.http_rule.HttpRule(
                                    rule_type = 'HttpRule', 
                                    methods = ["get"], 
                                    path_regex = '/.*', 
                                    query_parameters = [
                                        agilicus_api.models.rule_query_parameter.RuleQueryParameter(
                                            name = '0', 
                                            exact_match = '0', )
                                        ], 
                                    body = agilicus_api.models.rule_query_body.RuleQueryBody(
                                        json = [
                                            agilicus_api.models.rule_query_body_json.RuleQueryBodyJSON(
                                                name = '0', 
                                                exact_match = '0', 
                                                match_type = 'string', 
                                                pointer = '/foo/0/a~1b/2', )
                                            ], ), ), 
                                scope = 'anyone', ), )
                        ], 
                    scope = 'anyone', )
            )
        else :
            return CombinedRules(
                status = agilicus_api.models.combined_rules_status.CombinedRulesStatus(
                    app_id = '123', 
                    org_id = '123', 
                    role_id = '123', 
                    role_name = '0', 
                    rules = [
                        agilicus_api.models.rule_v2.RuleV2(
                            metadata = {"id":"ac233asaksjfF","created":"2017-07-07T15:49:51.230+00:00","updated":"2020-01-27T12:19:46.430+00:00"}, 
                            spec = agilicus_api.models.rule_spec.RuleSpec(
                                comments = 'This rule allows access to all static content of the application for any user, even if they are not authenticated.', 
                                condition = agilicus_api.models.http_rule.HttpRule(
                                    rule_type = 'HttpRule', 
                                    methods = ["get"], 
                                    path_regex = '/.*', 
                                    query_parameters = [
                                        agilicus_api.models.rule_query_parameter.RuleQueryParameter(
                                            name = '0', 
                                            exact_match = '0', )
                                        ], 
                                    body = agilicus_api.models.rule_query_body.RuleQueryBody(
                                        json = [
                                            agilicus_api.models.rule_query_body_json.RuleQueryBodyJSON(
                                                name = '0', 
                                                exact_match = '0', 
                                                match_type = 'string', 
                                                pointer = '/foo/0/a~1b/2', )
                                            ], ), ), 
                                scope = 'anyone', ), )
                        ], 
                    scope = 'anyone', ),
        )

    def testCombinedRules(self):
        """Test CombinedRules"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
