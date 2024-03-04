from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserGet(BaseCase):

    def test_get_user_details_auth_as_another_user(self):

        # New user registration
        new_user_data = self.prepare_registation_data()

        response1 = MyRequests.post("/user/", data=new_user_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        
        # New user login
        auth_data = {
            'email': new_user_data['email'],
            'password': new_user_data['password']
        }

        response2 = MyRequests.post("/user/login", data=auth_data)

        Assertions.assert_status_code(response1, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Get another user (id=2) info
        user_id = 2
        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response3, "username")
        Assertions.assert_json_has_not_key(response3, "email")
        Assertions.assert_json_has_not_key(response3, "firstName")
        Assertions.assert_json_has_not_key(response3, "lastName")        