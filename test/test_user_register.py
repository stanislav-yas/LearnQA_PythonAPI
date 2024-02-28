from datetime import datetime
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    def setup_method(self):
        email_base_part = "learnqa"
        domain = "example.com"
        email_random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{email_base_part}{email_random_part}@{domain}"

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email           
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode() == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}" 