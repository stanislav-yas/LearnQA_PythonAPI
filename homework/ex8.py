import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"
# step 1
response = requests.get(url=url)
result = response.json(); print(result)
seconds = result["seconds"]
token = result["token"]

# step 2
params = {"token": token}
response = requests.get(url=url, params=params)
result = response.json()
if 'error' in result:
    print(f"Error occured: {result['error']}")
    exit(1)

if 'status' in result and result["status"] == "Job is NOT ready":
    print(f"Job is NOT ready. Waiting {seconds} seconds...")

    # step 3
    time.sleep(seconds)

    # step 4
    response = requests.get(url=url, params=params)
    result = response.json()
    if 'status' not in result:
        print(f"Something was wrong with Job#{token}")
        exit(1)
    if result["status"] != "Job is ready":
        print(f"Job#{token} still not ready")
        exit(1)
    if 'result' not in result:
        print(f"No result returns with Job#{token}")
        exit(1)
    res = result["result"]
    print(f"Job#{token} done successfully with result={res}") # result=42
    exit(0)
else:
    print(f"Something was wrong with Job#{token}")
    exit(1)