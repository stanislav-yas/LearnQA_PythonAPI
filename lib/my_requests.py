import requests
import allure
from lib.logger import Logger

class MyRequests():
    def get(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._request('GET', url=url, data=data, headers=headers, cookies=cookies)

    def post(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
         with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._request('POST', url=url, data=data, headers=headers, cookies=cookies)

    def put(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
         with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._request('PUT', url=url, data=data, headers=headers, cookies=cookies)   

    def delete(url: str, data: dict=None, headers: dict=None, cookies: dict=None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._request('DELETE', url=url, data=data, headers=headers, cookies=cookies)

    @staticmethod
    def _request(method: str, url: str, data: dict={}, headers: dict={}, cookies: dict={}):
        url = f"https://playground.learnqa.ru/api{url}"

        Logger.add_request(method, url, data, headers, cookies)

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
        
        Logger.add_response(response)

        return response