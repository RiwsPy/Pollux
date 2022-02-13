from . import call as base_call

BASE_URL = "https://data.mobilites-m.fr"


def call(self, url: str, **kwargs) -> dict:
    url = BASE_URL + url

    return base_call(self, url=url)
