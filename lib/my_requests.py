import requests

class MyRequests():
    def get(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        return MyRequests._requests('GET', url=url, data=data, headers=headers, cookies=cookies)

    def post(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        return MyRequests._requests('POST', url=url, data=data, headers=headers, cookies=cookies)

    def put(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        return MyRequests._requests('PUT', url=url, data=data, headers=headers, cookies=cookies)   

    def delete(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        return MyRequests._requests('DELETE', url=url, data=data, headers=headers, cookies=cookies)

    @staticmethod
    def _request(method: str, url: str, data: dict={}, headers: dict={}, cookies: dict={}):
        url = f"https://playground.learnqa.ru/api{url}"
        if method == 'GET':
            response = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers, cookies=cookies)  
        elif method == 'DELETE':
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        return response