import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
redirect_cnt = len(response.history)
if redirect_cnt > 0:
    print(f"Request was redirected {redirect_cnt} time(s)")
    for resp in response.history:
        print(f"{resp.status_code}:{resp.url}")
else:
    print("No redirection")

print(f"{response.status_code}: {response.url}")