import requests

response = requests.get("https://playground.learnqa.ru/api/get_500")
print(response.status_code)

response = requests.post("https://playground.learnqa.ru/api/something")
print(response.status_code)

response = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True)

if len(response.history) > 0:
    print(response.history[0].status_code)
    print(response.history[0].url); 

print(response.status_code)
print(response.url); 
