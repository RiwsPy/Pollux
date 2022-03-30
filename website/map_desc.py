DESC1 = """
Tuto ?

Sur cette carte vous êtes invités à créer votre propre zone de recherche.
Une fois fait, Pollux identifie les différents éléments présents dans cette zone.
Dans le panneau de droite, s'affichera des recommandations d'éclairage en fonction de ceux-ci.

En passant votre souris sur la forme créée, s'affichera le nombre des différents éléments trouvés.

La façon la plus élémentaire pour créer une zone, c'est de cliquer sur la carte.
Un clic crée immédiatement un cercle d'un rayon de 10 mètres.
Toutefois, si vous créez un second cercle sur la carte, le premier cercle disparaîtra.

Il est possible de créer d'autres formes grâce à la barre de dessin sur la gauche.


Il est également possible de déplacer, de modifier ou de supprimer les formes créées.

En haut à droite, se trouve le bouton Calque.
Il vous permet de visualiser finement où se trouve chaque élément.
En cliquant sur ces éléments, diverses informations sont renseignées comme par exemple l'espèce de l'arbre ou le nom de la ligne de bus.
"""

DESC2 = """
Pleins de trucs ici, trop faciles à lire.
"""

DESC3 = """
Cette carte de chaleur part du postolat suivant :
Les luminaires éclairent les rues mais aussi la biodiversité à proximité.
Cette carte permet de visualiser l'impact des luminaires sur la faune et la flore locale.
Chaque luminaire va se voir affecter une note d'impact.
Cette note dépend essentiellement de deux facteurs :
* La proximité de l'objet avec la source lumineuse
* La quantité d'objets éclairés par la source lumineuse

Le tout est présenté sous le format d'une carte de chaleur afin de pouvoir couvrir une large zone.
Les zones aux couleurs chaudes représentant les zones où les luminaires ont un impact important.
A l'inverse les zones non colorées représentent des zones où l'impact constaté est nul.
Par convention, ont un impact maximal (1), les luminaires ayant un arbre à moins de 3 mètres de leur source lumineuse.

Cette carte présente 3 calques
* Sans filtre : qui va afficher la carte selon la note d'impact du luminaire, sans prendre en compte l'heure de la journée.
Il s'agit du filtre qui présente, de façon excessive, l'impact des luminaires, il peut servir de comparatif avec les deux filtres suivants.

Les luminaires peuvent posséder une température de couleur (K) basse (compatible avec la biodiversité) ou posséder plusieurs régimes : leur intensité lumineuse varie selon l'heure de la nuit.
Pour représenter ce paramètre, deux filtres sont disponibles :
* Jour (ou début de soirée) : sont retirés les luminaires ayant une température de couleur inférieure ou égale à 2500K, ainsi que ceux fonctionnant avec des détecteurs de présence.
* Nuit : c'est le calque Jour avec un filtre supplémentaire : sont également retirés les luminaires présentant une baisse de leur intensité au cours de la nuit. 


"""