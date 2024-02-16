import requests

headers = {"my_header": "my_header_value"}
response = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
print(f"Request headers: {response.text}")
print(f"Response headers: {response.headers}")
