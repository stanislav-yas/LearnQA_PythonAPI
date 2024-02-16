import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods1 = ['POST', 'GET', 'PUT', 'DELETE']
methods2 = ['HEAD', 'OPTIONS', 'PATCH']

# step 1
print("\nStep 1\n------")
for method in methods1:
    response = requests.request(method=method, url=url)
    print(f"{response.status_code}:{response.text} - {response.request.method}")

# step 2
print("\nStep 2\n------")
for method in methods2:
    response = requests.request(method=method, url=url)
    print(f"{response.status_code}:{response.text} - {response.request.method}")

# step 3
print("\nStep 3\n------")    
for method in methods1:
    params = {"method":{method}}
    if method == 'GET':
        response = requests.request(method=method, url=url, params=params)
    else:
        response = requests.request(method=method, url=url, data=params)
    print(f"{response.status_code}:{response.text} - {response.request.method}:{method}")

# step 4
print("\nStep 4\n------")
for method in methods1+methods2:
    for param_method in methods1+methods2:  
        params = {"method":{param_method}}
        if method == 'GET':
            response = requests.request(method=method, url=url, params=params)
        else:
            response = requests.request(method=method, url=url, data=params)
        print(f"{response.status_code}:{response.text} - {response.request.method}:{param_method}")