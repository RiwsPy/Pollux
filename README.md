# Projet Pollux

Projet Pollux dans le cadre du CivicLab de Grenoble, proposé par la Fabrique.coop.
Pour le défi *Lux, Led, Lumens* porté par GreenAlp.
https://grenoble.civiclab.eu


Le prototype du projet est visible sur : https://green-pollux.herokuapp.com


### Prérequis:
* Python3
* pipenv


### Téléchargement :
```
git clone https://github.com/RiwsPy/Pollux.git
```

### Installation :
```
cd Pollux/
pipenv install
pipenv shell
```

### Démarrage de l'application :
```
./engine.py
```

En local, par défaut, l'application sera visible sur l'url :
http://127.0.0.1:5000/


### Architecture:
- .env
- Pipfile
- Pipfile.lock
- Procfile
- api_ext/
    - clips.py
    - grenoble_alpes_metropole.py
    - osm.py
    - smmag.py
- db/
- formats/
- website/
    - static/
        - css/
        - fonts/
        - img/
        - js/
    - templates/
        - index.html
        - map.html
        - ...
    - views.py
- works/
    - acccidents.py
    - birds.py
    - ...


### Pollux API :
Cette application utilise de nombreux jeux de données issus notamment de la métropole de Grenoble ainsi que de OpenStreetMap.
Chaque jeu de données est représenté par un fichier .py présent dans le dossier *Works*.

Fichier Works | Contenu | Origine des données | Mise à jour automatique | Détails
 --- | --- | ---  | --- | ---
accidents | Accidents de voiture 2019-2020 | https://www.data.gouv.fr/fr/ | Non | Le format csv a évolué en 2019
birds | Observations d'oiseaux 2012-2021 | https://openobs.mnhn.fr/ | Non | Récupération contraingnante
crossings | Passages piétons | https://overpass-turbo.eu/ (OpenStreetMap) | Oui | /
highways | Artères principales de Grenoble | / | Non | Retranscription manuelle
lamps | Emplacement des luminaires | Non | Données pas encore disponibles
parks | Parcs | https://overpass-turbo.eu/ (OpenStreetMap) | Oui | /
shops | Bâtiments dont les horaires d'ouverture sont connues | https://overpass-turbo.eu/ (OpenStreetMap) | Oui | /
tc_stops | Arrêts de bus | https://data.metropolegrenoble.fr/ | Oui | /
tc_ways | Voies de bus | https://data.metropolegrenoble.fr/ | Oui | /
trees | Arbres | https://data.metropolegrenoble.fr/ | Oui | /


Ces données étant sous licence ouverte, il nous a paru évident de redistribuer ces informations ainsi que celles générées par Pollux.
Les requêtes passent l'endpoint **api/**.

```
https://green-pollux.herokuapp.com/api/crossings_output.json
```

3 types de données sont présentes :
* Les données originelles, par exemple *parks.json*, *tc_stops.json*
* Les données filtrées par Pollux, elles portent le même nom que le fichier originel mais se termine par *_output* : *parks_output.json*, *tc_stops_output.json*
* Les données créées ou enrichies par Pollux : *conflict_lamps__trees_birds.json* (qui est la base utilisée par la carte Impact)


### Tests :
Les tests sont réalisés par **pytest**.
Actuellement, seule la partie backend est testée, la couverture est de 93%.

```
pytest
```
ou bien
```
coverage run -m pytest
```


### Les mises à jour automatique des données :
Certaines données se prêtent très bien aux mises à jour. D'autres pas du tout.


Pour mettre à jour toutes les bases de données, excécutez la méthode suivante :
```
./engine.py -uDB
```

Il est possible de cibler précisément une ou plusieurs bases, par exemple :
```
./engine.py -uDB parks shops
```

