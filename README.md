# Projet Pollux

Projet Pollux dans le cadre du CivicLab de Grenoble, proposé par la Fabrique.coop.
https://grenoble.civiclab.eu


Le projet est visible sur : http://green-pollux.heroku.app.com


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

Par défaut, l'application sera visible sur l'url :
http://127.0.0.1:5000/

### Architecture:
- .env
- Pipfile
- Pipfile.lock
- api_ext/
    - grenoble_alpes_metropole.py
    - osm.py
- db/
- entities/
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
    - views.py
- works/


### API :
Cette application utilise des données issues de la métropole de Grenoble ainsi que de OpenStreetMap.
Cette application peut elle-même être utilisée comme une API REST via l'endpoint /api/.
