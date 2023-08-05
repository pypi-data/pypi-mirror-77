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

import agilicus_api
from agilicus_api.api.applications_api import ApplicationsApi  # noqa: E501
from agilicus_api.rest import ApiException


class TestApplicationsApi(unittest.TestCase):
    """ApplicationsApi unit test stubs"""

    def setUp(self):
        self.api = agilicus_api.api.applications_api.ApplicationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_config(self):
        """Test case for add_config

        Add an environment configuration row  # noqa: E501
        """
        pass

    def test_add_role(self):
        """Test case for add_role

        Add a role to the application.  # noqa: E501
        """
        pass

    def test_add_role_to_rule_entry(self):
        """Test case for add_role_to_rule_entry

        Add a rule to a role in the application.  # noqa: E501
        """
        pass

    def test_add_rule(self):
        """Test case for add_rule

        Add a rule to the application.  # noqa: E501
        """
        pass

    def test_create_application(self):
        """Test case for create_application

        Create an application  # noqa: E501
        """
        pass

    def test_delete_application(self):
        """Test case for delete_application

        Remove an application  # noqa: E501
        """
        pass

    def test_delete_config(self):
        """Test case for delete_config

        Remove an environment configuration  # noqa: E501
        """
        pass

    def test_delete_role(self):
        """Test case for delete_role

        Remove a role  # noqa: E501
        """
        pass

    def test_delete_role_to_rule_entry(self):
        """Test case for delete_role_to_rule_entry

        Remove a role_to_rule_entry  # noqa: E501
        """
        pass

    def test_delete_rule(self):
        """Test case for delete_rule

        Remove a rule  # noqa: E501
        """
        pass

    def test_get_application(self):
        """Test case for get_application

        Get a application  # noqa: E501
        """
        pass

    def test_get_config(self):
        """Test case for get_config

        Get environment configuration  # noqa: E501
        """
        pass

    def test_get_environment(self):
        """Test case for get_environment

        Get an environment  # noqa: E501
        """
        pass

    def test_get_role(self):
        """Test case for get_role

        Get a role  # noqa: E501
        """
        pass

    def test_get_role_to_rule_entry(self):
        """Test case for get_role_to_rule_entry

        Get a role_to_rule_entry  # noqa: E501
        """
        pass

    def test_get_rule(self):
        """Test case for get_rule

        Get a rule  # noqa: E501
        """
        pass

    def test_list_applications(self):
        """Test case for list_applications

        Get applications  # noqa: E501
        """
        pass

    def test_list_combined_rules(self):
        """Test case for list_combined_rules

        List rules combined by scope or role  # noqa: E501
        """
        pass

    def test_list_configs(self):
        """Test case for list_configs

        Get all environment configuration  # noqa: E501
        """
        pass

    def test_list_environment_configs_all_apps(self):
        """Test case for list_environment_configs_all_apps

        Get all environment configuration for a given organisation.  # noqa: E501
        """
        pass

    def test_list_role_to_rule_entries(self):
        """Test case for list_role_to_rule_entries

        Get all RoleToRuleEntries  # noqa: E501
        """
        pass

    def test_list_roles(self):
        """Test case for list_roles

        Get all roles  # noqa: E501
        """
        pass

    def test_list_rules(self):
        """Test case for list_rules

        Get all rules  # noqa: E501
        """
        pass

    def test_list_runtime_status(self):
        """Test case for list_runtime_status

        Get an environment's runtime status  # noqa: E501
        """
        pass

    def test_replace_application(self):
        """Test case for replace_application

        Create or update an application  # noqa: E501
        """
        pass

    def test_replace_config(self):
        """Test case for replace_config

        Update environment configuration  # noqa: E501
        """
        pass

    def test_replace_environment(self):
        """Test case for replace_environment

        Update an environment  # noqa: E501
        """
        pass

    def test_replace_role(self):
        """Test case for replace_role

        Update a role  # noqa: E501
        """
        pass

    def test_replace_role_to_rule_entry(self):
        """Test case for replace_role_to_rule_entry

        Update a role_to_rule_entry  # noqa: E501
        """
        pass

    def test_replace_rule(self):
        """Test case for replace_rule

        Update a rule  # noqa: E501
        """
        pass

    def test_replace_runtime_status(self):
        """Test case for replace_runtime_status

        update an environemnt's runtime status  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
