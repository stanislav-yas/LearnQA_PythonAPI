from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Тесты метода GET")
class TestUserGet(BaseCase):

    @allure.title("Not authorized getting user info")
    @allure.description("Проверка получаемых полей пользователя не будучи авторизованным")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Getting by an authorized user of their credentials")
    @allure.description("Проверка получения авторизованным пользователем всех полей своих учётных данных")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login" , data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    allure.title("Authorized getting another user info")
    @allure.description("Проверка получения авторизованным пользователем полей чужых учётных данных.\
                        Должно быть доступно только поле 'username'")    
    def test_get_user_details_auth_as_another_user(self):

        with allure.step("New user registration"):
            new_user_data = self.prepare_registation_data()

            response1 = MyRequests.post("/user/", data=new_user_data)

            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")
        
        with allure.step("New user login"):
            auth_data = {
                'email': new_user_data['email'],
                'password': new_user_data['password']
            }

            response2 = MyRequests.post("/user/login", data=auth_data)

            Assertions.assert_status_code(response2, 200)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        with allure.step("Getting another user (id=2) info"):
            user_id = 2
            response3 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_status_code(response3, 200)
            Assertions.assert_json_has_key(response3, "username")
            Assertions.assert_json_has_not_key(response3, "email")
            Assertions.assert_json_has_not_key(response3, "firstName")
            Assertions.assert_json_has_not_key(response3, "lastName")        
        