from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Тесты метода PUT")
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

    @allure.title("Edit just created user")
    @allure.description("Тест на редактирование своих данных авторизованным пользователем")
    def test_edit_just_created_user(self):

        with allure.step("User login (created in setup)"):
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

        with allure.step("Try to change user firstName"):
            new_name = "Changed Name"

            response2 = MyRequests.put(
                f"/user/{self.user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_status_code(response2, 200)

        with allure.step("Changed data verifying"):
            response3 = MyRequests.get(
                f"/user/{self.user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

            Assertions.assert_json_value_by_name(
                response3,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    @allure.title("Attempt not authorized user info edition")
    @allure.description("Попытаемся изменить данные пользователя, будучи неавторизованными")
    def test_edit_not_auth(self):
        new_firstName = "Changed Name"

        response = MyRequests.put(
            f"/user/{self.user_id}",
            data={'firstName': new_firstName}
        )
        Assertions.assert_status_code(response, 400)
        Assertions.assert_json_has_key(response, 'error')
        assert self.get_json_value(response, 'error') == "Auth token not supplied", f"Unexpected response content {response.text}"

    @allure.title("Attempt authorized edition of another user info")
    @allure.description("Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем")
    def test_edit_auth_another_user(self):

        with allure.step("Login User#1 (created in setup)"):
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

        with allure.step("Register User#2"):
            user2_data = self.prepare_registation_data()
            response2 = MyRequests.post("/user/", data=user2_data)

            Assertions.assert_status_code(response2, 200)
            Assertions.assert_json_has_key(response2, 'id')

            user2_email = user2_data['email']
            user2_password = user2_data['password']
            user2_firstName = user2_data['firstName']
            user2_id = self.get_json_value(response2, 'id')

        with allure.step("Changing User#2 info by User#1"):
            user2_new_name = "Changed Name"
            response3 = MyRequests.put(
                f"/user/{user2_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": user2_new_name}
            )
            Assertions.assert_status_code(response3, 200)

        with allure.step("Login User#2"):
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

        with allure.step("User#2 info changing verification"):    
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

    @allure.title("Attempt authorized change of user email by incorrect value")
    @allure.description("Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @ ")
    def test_edit_email_auth(self):
        with allure.step("Login User (created in setup)"):
            user_data = {
                'email': self.user_email,
                'password': self.user_password
            }
            response1 = MyRequests.post("/user/login", data=user_data)
            Assertions.assert_status_code(response1, 200)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        with allure.step("Attempt to change of User email"):
            new_email = "user.mail.com" # no '@' in email
            response2 = MyRequests.put(
                f"/user/{self.user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": new_email}
            )
            Assertions.assert_status_code(response2, 400)
            Assertions.assert_json_has_key(response2, 'error')
            assert self.get_json_value(response2, 'error') == 'Invalid email format', f"Unexpected response content: {response2.text}"

    @allure.title("Attempt authorized change of user firstName by very short value")
    @allure.description("Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, \
                        на очень короткое значение в один символ")
    def test_edit_short_firstName_auth(self):
        
        with allure.step("Login User (created in setup)"):
            user_data = {
                'email': self.user_email,
                'password': self.user_password
            }
            response1 = MyRequests.post("/user/login", data=user_data)
            Assertions.assert_status_code(response1, 200)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        with allure.step("#Attempt to change of User first name"):
            new_firstName = "a" # a very short first name
            response2 = MyRequests.put(
                f"/user/{self.user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_firstName}
            )
            Assertions.assert_status_code(response2, 400)
            assert self.get_json_value(response2, 'error') == 'The value for field `firstName` is too short', \
                f"Unexpected response content: {response2.text}"
