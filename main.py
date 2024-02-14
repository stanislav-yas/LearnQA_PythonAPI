import requests
from json.decoder import JSONDecodeError

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

try:
    parsed_response_text = response.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Response is not a JSON format")
    