from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Тесты на DELETE")
class TestUserDelete(BaseCase):

    def setup_method(self):
        # A new user registration
        user_data = self.prepare_registation_data()
        response1 = MyRequests.post("/user/", data=user_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.user_email = user_data['email']
        self.user_password = user_data['password']
        self.user_id = self.get_json_value(response1, "id")

    @allure.description("Попытка удалить пользователя с ID 2")
    def test_delete_user_id_2(self):
        # Login as user ID 2
        response1 = MyRequests.post(
            "/user/login", 
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
        )
        Assertions.assert_status_code(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Try to delete user with ID=2     
        user2_id = 2

        response2 = MyRequests.delete(
            f"/user/{user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response2, 400)
        assert response2.text == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"Unexpected response content: {response2.text}"

    @allure.description("Позитивный тест на удаление пользователя")
    def test_delete_user_auth(self):
        # Login as a new user (created in setup)
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

        # Try to delete a new user   
        response2 = MyRequests.delete(
            f"/user/{self.user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response2, 200)

        # Checking a new user deletion
        response3 = MyRequests.get(
            f"/user/{self.user_id}"
        )

        Assertions.assert_status_code(response3, 404)
        assert response3.text == 'User not found', f"Unexpected response content: {response3.text}"

    @allure.description("Попробовать удалить пользователя, будучи авторизованными другим пользователем")
    def test_delete_user_auth_another_user(self):
        # Login as user #1 (created in setup)
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

        # New user #2 registration
        user2_data = self.prepare_registation_data()
        response2 = MyRequests.post("/user/", data=user2_data)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, 'id')
        user2_id = self.get_json_value(response2, 'id')

        # Try to delete another user (just created user #2)     
        response3 = MyRequests.delete(
            f"/user/{user2_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response3, 200)

        # Checking the user #2 are not deleted
        response4 = MyRequests.get(
            f"/user/{user2_id}"
        )

        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_has_key(response4, 'username')
