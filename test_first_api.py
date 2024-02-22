import requests

class TestFirstAPI:
    def test_hello_call(self):
        url = "https://playground.learnqa.ru/api/hello"
        name = 'Stanislav'
        data = {'name': name}

        response = requests.get(url, params=data)

        assert response.status_code == 200, f"Wrong response code{response.status_code}"

        response_dict = response.json()
        assert "answer" in response_dict, "There is no field 'answer' in the response"

        expected_response_text = f"Hello, {name}"
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, f"Actual text in the response is not correct: {actual_response_text}"
