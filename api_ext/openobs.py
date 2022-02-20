from . import call as base_call

# datasets : nb de jeu de db
# occurrences : nb d'observation

def call(self, url: str, **kwargs) -> dict:
    url = "https://openobs.mnhn.fr/api/" + url

    return base_call(self, url=url, method="get")
