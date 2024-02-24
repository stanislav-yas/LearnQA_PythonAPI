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
