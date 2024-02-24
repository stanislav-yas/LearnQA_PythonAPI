import requests

def test_check_header():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    headers = response.headers
    #print(headers)
    header_name = 'x-secret-homework-header'
    assert header_name in headers, f"Response doesn't contain '{header_name}' header"

    header_value = headers[header_name]
    assert header_value == 'Some secret value', f"Invalid header value: '{header_value}'"