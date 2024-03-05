from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Негативные тесты на PUT")
class TestUserEdit(BaseCase):

    def setup_method(self):
        # New user registration
        user_data = self.prepare_registation_data()
        response1 = MyRequests.post("/user/", data=user_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.user_email = user_data['email']
        self.user_password = user_data['password']
        self.user_id = self.get_json_value(response1, "id")       

    @allure.description("Попытаемся изменить данные пользователя, будучи неавторизованными")
    def test_edit_not_auth(self):
        new_firstName = "Changed Name"

        response = MyRequests.put(
            f"/user/{self.user_id}",
            data={'firstName': new_firstName}
        )
        Assertions.assert_status_code(response, 400)
        assert response.text == "Auth token not supplied", f"Unexpected response content {response.text}"

    @allure.description("Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем")
    def test_edit_auth_another_user(self):
        # Login User1
        response1 = MyRequests.post(
            "/user/login", 
            data = {
                'email': self.user_email,
                'password': self.user_password
            }
        )
        Assertions.assert_status_code(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Creation User2
        user2_data = self.prepare_registation_data()
        response2 = MyRequests.post("/user/", data=user2_data)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, 'id')

        user2_email = user2_data['email']
        user2_password = user2_data['password']
        user2_firstName = user2_data['firstName']
        user2_id = self.get_json_value(response2, 'id')

        # Changing User2 data
        user2_new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": user2_new_name}
        )
        Assertions.assert_status_code(response3, 200)

        # Login User2
        response4 = MyRequests.post(
            "/user/login", 
            data = {
                'email': user2_email,
                'password': user2_password
            }
        )
        Assertions.assert_status_code(response4, 200)
        auth_sid = self.get_cookie(response4, "auth_sid")
        token = self.get_header(response4, "x-csrf-token")

        # Check User2 data change      
        response5 = MyRequests.get(
            f"/user/{user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_status_code(response5, 200)
        Assertions.assert_json_value_by_name(
            response5,
            "firstName",
            user2_firstName,
            "First name of user was changed by another user!"
        )

    @allure.description("Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @ ")
    def test_edit_email_auth(self):
        # Login User
        user_data = {
            'email': self.user_email,
            'password': self.user_password
        }
        response1 = MyRequests.post("/user/login", data=user_data)
        Assertions.assert_status_code(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Changing User email
        new_email = "user.mail.com" # no '@' in email
        response2 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_status_code(response2, 400)
        assert response2.text == 'Invalid email format', f"Unexpected response content: {response2.text}"

    @allure.description("Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, \
                        на очень короткое значение в один символ")
    def test_edit_short_firstName_auth(self):
         # Login User
        user_data = {
            'email': self.user_email,
            'password': self.user_password
        }
        response1 = MyRequests.post("/user/login", data=user_data)
        Assertions.assert_status_code(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Changing User first name
        new_firstName = "a" # a very short first name
        response2 = MyRequests.put(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_firstName}
        )
        Assertions.assert_status_code(response2, 400)
        assert self.get_json_value(response2, 'error') == 'Too short value for field firstName', \
            f"Unexpected response content: {response2.text}"
