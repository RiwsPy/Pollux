from . import call as base_call


def call(self, url: str, **kwargs) -> dict:
    url = "http://entrepot.metropolegrenoble.fr/" + url

    return base_call(self, url=url)
