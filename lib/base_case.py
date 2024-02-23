from requests import Response
from requests.exceptions import JSONDecodeError
import pytest

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"No cookie '{cookie_name} in the response'"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"No cookie '{header_name} in the response'"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except JSONDecodeError:
            pytest.fail(f"Response is not JSON Format: '{response.text}'")

        assert name in response_as_dict, f"Response JSON doesn't contain a key '{name}'"
        return response_as_dict[name]
