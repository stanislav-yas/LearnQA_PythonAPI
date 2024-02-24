import requests

def test_check_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    #print(response.cookies)
    assert len(response.cookies) > 0, "The response doesn't contain any cookie"
    cookie_value = response.cookies.get('HomeWork')
    assert cookie_value is not None, f"The response doesn't contain 'HomeWork' cookie"
    assert cookie_value == 'hw_value', f"Invalid value of 'HomeWork' cookie: {cookie_value}"