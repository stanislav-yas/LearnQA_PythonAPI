import requests

params = {"name": "Stas"}
response = requests.get("https://playground.learnqa.ru/api/check_type", params=params)
print(response.text)

response = requests.put("https://playground.learnqa.ru/api/check_type", data=params)
print(response.text)
