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
from agilicus_api.api.challenges_api import ChallengesApi  # noqa: E501
from agilicus_api.rest import ApiException


class TestChallengesApi(unittest.TestCase):
    """ChallengesApi unit test stubs"""

    def setUp(self):
        self.api = agilicus_api.api.challenges_api.ChallengesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_challenge(self):
        """Test case for create_challenge

        create a challenge  # noqa: E501
        """
        pass

    def test_create_totp_enrollment(self):
        """Test case for create_totp_enrollment

        create a TOTP challenge enrollment  # noqa: E501
        """
        pass

    def test_create_webauthn_enrollment(self):
        """Test case for create_webauthn_enrollment

        create a WebAuthN challenge enrollment  # noqa: E501
        """
        pass

    def test_delete_challenge(self):
        """Test case for delete_challenge

        Delete the challenge specified by challenge_id  # noqa: E501
        """
        pass

    def test_delete_totp_enrollment(self):
        """Test case for delete_totp_enrollment

        Delete the TOTP enrollment specified by totp id  # noqa: E501
        """
        pass

    def test_delete_webauthn_enrollment(self):
        """Test case for delete_webauthn_enrollment

        Delete the WebAuthN enrollment specified by webauthn_id  # noqa: E501
        """
        pass

    def test_get_answer(self):
        """Test case for get_answer

        answer a challenge  # noqa: E501
        """
        pass

    def test_get_challenge(self):
        """Test case for get_challenge

        Get the challenge specified by challenge_id  # noqa: E501
        """
        pass

    def test_get_totp_enrollment(self):
        """Test case for get_totp_enrollment

        Get the TOTP enrollment specified by totp_id  # noqa: E501
        """
        pass

    def test_get_webauthn_enrollment(self):
        """Test case for get_webauthn_enrollment

        Get the WebAuthN enrollment specified by webauthn_id  # noqa: E501
        """
        pass

    def test_list_totp_enrollment(self):
        """Test case for list_totp_enrollment

        List the totp enrollment results  # noqa: E501
        """
        pass

    def test_list_webauthn_enrollments(self):
        """Test case for list_webauthn_enrollments

        List the webauthn enrollments  # noqa: E501
        """
        pass

    def test_replace_challenge(self):
        """Test case for replace_challenge

        Replace the challenge specified by challenge_id  # noqa: E501
        """
        pass

    def test_update_totp_enrollment(self):
        """Test case for update_totp_enrollment

        Update the totp_enrollment if the answer provided is correct. This moves the state from pending to success.  # noqa: E501
        """
        pass

    def test_update_webauthn_enrollment(self):
        """Test case for update_webauthn_enrollment

        Update the WebAuthN enrollment if the answer provided is correct. This completes the device enrollment.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
