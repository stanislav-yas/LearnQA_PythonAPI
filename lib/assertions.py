from requests import Response
import json
import pytest


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            pytest.fail(f"Response is not JSON Format: '{response.text}'")
        assert name in response_as_dict, f"Response JSON doesn't contain a key '{name}'"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format: '{response.text}'"
        assert key in response_as_dict, f"Response JSON doesn't contain a key '{key}'"

    @staticmethod
    def assert_json_has_keys(response: Response, keys):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON Format: '{response.text}'"
        for key in keys:
            assert key in response_as_dict, f"Response JSON doesn't contain a key '{key}'"

    @staticmethod
    def assert_json_has_not_key(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON Format: '{response.text}'"
        assert key not in response_as_dict, f"Response JSON contain a key '{key}'"        

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Unexpected status code: {response.status_code}, \
            expected: {expected_status_code}"