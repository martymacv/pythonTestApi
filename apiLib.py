import requests

from testDocs import *


class Store(TestCase):
    def __init__(self, base_url):
        super().__init__()
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url


class BaseApiTestStep(TestStep):
    def __init__(self, name, base_url):
        super().__init__(name)
        self.__base_url = base_url
        self.__path = ""
        self.__headers = {
            'Authorization': 'token special-key'
        }
        self.__body = dict()
        self.__params = ""
        self.__response = None

    @property
    def response(self):
        return self.__response

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @logger
    def action_get(self, params=None):
        if params is None:
            params = dict()
        if 'in_path' in params:
            self.__path = self.__path.format(**params['in_path'])
        if 'in_query' in params:
            self.__params = '?' + '&'.join([f"{key}={value}" for key, value in params['in_query'].items()])
        if 'in_body' in params:
            self.__body.update(params['in_body'])
        if 'in_headers' in params:
            self.__headers.update((params['in_headers']))
        url_pack = self.__base_url + self.__path
        exc_info = None
        try:
            self.__response = requests.get(url=url_pack, headers=self.__headers, json=self.__body)
        except Exception as e:
            exc_info = str(e)
        return {
            "action": url_pack,
            'exc_info': exc_info
        }

    @logger
    def check_status_code(self, expected: int):
        actual = None
        exc_info = None
        try:
            actual = self.response.status_code
        except Exception as e:
            exc_info = str(e)
        return {
            'check_desc': "Проверка статус кода",
            'check_result': actual == expected,
            'actual': actual,
            'exc_info': exc_info
        }


class GetStoreInventory(BaseApiTestStep):
    def __init__(self, name, base_url):
        super().__init__(name, base_url)
        self.path = "/store/inventory"

    @logger
    def check_pets_status(self, expected: int):
        actual = None
        exc_info = None
        try:
            actual = len(self.response.json())
        except Exception as e:
            exc_info = str(e)
        return {
            'check_desc': "Проверка полноты статусов питомцев",
            'check_result': actual >= expected,
            'actual': actual,
            'exc_info': exc_info
        }
