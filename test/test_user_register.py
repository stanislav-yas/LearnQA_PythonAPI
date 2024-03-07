from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure
import pytest
from random import choice
import string

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    @allure.title("User registration test")
    @allure.description("Позитивный тест на регистрацию пользователя")
    def test_create_user_successfully(self):
        data = self.prepare_registation_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Attemt to register a user with existing email")
    @allure.description("Попытка создания пользователя с уже зарегистрированным в системе 'email'")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registation_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode() == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}" 

    @allure.title("Attemt to register a user having not valid email")
    @allure.description("Создание пользователя с некорректным email - без символа @")
    def test_invalid_email(self):
        email = "invalid.mail.com"
        data = self.prepare_registation_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.text == "Invalid email format", f"Unexpected response content {response.text}"

    registration_fields = [
        ('password'),
        ('username'),
        ('firstName'),
        ('lastName'),
        ('email')
    ]

    name_fields = [
        ('username'),
        ('firstName'),
        ('lastName'),        
    ]

    @allure.title("Attemt to register a user without any required field")
    @allure.description("Создание пользователя без указания одного из полей")
    @pytest.mark.parametrize('field', registration_fields)
    def test_without_one_of_the_fields(self, field):
        data = self.prepare_registation_data()
        data.pop(field) # delete a field from the registration data

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.text == f"The following required params are missed: {field}", f"Unexpected response content {response.text}"

    @allure.title("Attemt to register a user with a very short name")
    @allure.description("Создание пользователя с очень коротким именем в один символ")
    @pytest.mark.parametrize('name_field', name_fields)
    def test_too_short_name(self, name_field):
        data = self.prepare_registation_data()
        data[name_field] = 'a' # one symbol length name
         
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response, 400)
        assert response.text == f"The value of '{name_field}' field is too short", f"Unexpected response content {response.text}"        

    @allure.title("Attemt to register a user with a very long name")
    @allure.description("Создание пользователя с очень длинным именем - длиннее 250 символов")
    @pytest.mark.parametrize('name_field', name_fields)
    def test_too_long_name(self, name_field):
        data = self.prepare_registation_data()
        data[name_field] = ''.join(choice(string.ascii_letters) for _ in range(251)) # 251 symbol length name
         
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response, 400)
        assert response.text == f"The value of '{name_field}' field is too long", f"Unexpected response content {response.text}"          