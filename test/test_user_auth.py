import requests
import pytest

from lib.base_case import BaseCase

class TestUserAuth(BaseCase):

    #  Conditions for test_negative_auth_check
    conditions = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")  

    def test_auth_user(self):
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={
                "x-csrf-token": self.token
            },
            cookies={
                "auth_sid": self.auth_sid
            }
        )

        user_id_from_check_method = self.get_json_value(response2, "user_id")

        assert self.user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal to user is from check method"

    @pytest.mark.parametrize('condition', conditions)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={
                    "x-csrf-token": self.token
                }
            )
        elif condition == "no_token":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={
                    "auth_sid": self.auth_sid
                }
            )
        else:
            pytest.fail(f"Unknown condition: {condition}")

        user_id_from_check_method = self.get_json_value(response2, "user_id")

        assert user_id_from_check_method == 0, f"User was authorized with condition {condition}"