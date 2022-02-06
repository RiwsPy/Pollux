## Règles diverses pour l'équipe de développement :

### Tests :
Les tests sont réalisés avec pytest.


### Base de données :
Actuellement, le projet ne requiert pas de base de données relationnelles, les données sont stockées dans des fichiers .json (dossier db/).
En cas d'évolution, une base *postgreSQL* sera à privilégier.


### Variables d'environnement
La librairie *dotenv* permet d'utiliser facilement des variables d'environnement.
Pour cela il suffit de compléter le fichier *.env* présent à la racine (**attention**, en théorie, ce fichier n'est pas présent sur un repo, attention aux informations que vous y glissez).
Exemple :
```
VARTEST=42
```

Puis de l'appeler via :
```
import os
os.getenv('VARTEST')
```

### Flake8

Pour le code Python, merci d'appliquer autant que possible les normes de la PEP8.
Exécutez simplement cette commande à la racine du projet puis amusez-vous à corriger les notifications (si si c'est marrant).
```
flake8
```

### Langue

L'interface est en français car à destination de ceux-ci.
Néanmoins, les variables, commentaires, docstrings... Sont à rédiger autant que possible en anglais.
