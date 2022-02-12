import requests


class BadStatusError(Exception):
    pass


def call(self, **kwargs) -> dict:
    try:
        req = requests.request(method='GET', **kwargs)
    except requests.exceptions.ConnectionError:
        print('Erreur connexion.')
        raise requests.exceptions.ConnectionError

    if req.status_code != 200:
        print('ERROR status_code', req.status_code)
        raise BadStatusError

    return req.json()
