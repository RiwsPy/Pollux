import requests


class BadStatusError(Exception):
    pass


class Api_ext:
    method = 'GET'
    BASE_URL = 'http://127.0.0.1:8000'

    def call(self, **kwargs) -> dict:
        kwargs['method'] = kwargs.get('method', self.method)
        if 'url' in kwargs:
            kwargs['url'] = self.BASE_URL + str(kwargs['url'])

        try:
            req = requests.request(**kwargs)
        except requests.exceptions.ConnectionError:
            print('Erreur connexion.')
            raise requests.exceptions.ConnectionError

        if req.status_code != 200:
            print('ERROR status_code', req.status_code)
            raise BadStatusError

        return req.json()
