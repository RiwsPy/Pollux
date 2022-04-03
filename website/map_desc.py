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
L'objectif de la carte de contradiction est d'identifier les zones où sont présents des éléments dont les impacts sur la politique d'éclairage sont opposés.
Ici, les passages piétons et les magasins sont opposés à la biodiversité.
En effet, les passages piétons représentent une zone d'insécurité où une forte intensité lumineuse et un excellent rendu des couleurs sont attendus.
Les magasins attirent les citoyens ce qui génère des zones à usage important.

Pour ces deux raisons, l'éclairage public s'oriente vers des luminaires avec une puissance élevée, avec une température de couleur élevée.
En contradiction avec la biodiversité, qui préviligie des zones peu ou pas éclairées et une température de couleur basse.

Pour chacune de ces zones, Pollux calcule une valeur de contradiction qui dépend de la densité des éléments identifiés comme contradictoires et de la distance entre eux.

Cette valeur est traduite sur une échelle de couleur allant du rouge (niveau élevé) au violet (niveau faible).


3 calques sont disponibles sur cette carte :
* Jour : tous les éléments (passages piétons, magasins, biodiversité) sont pris en compte. Sont visibles les zones de contradiction en début de soirée.
* Nuit : les magasins sont considérés comme fermés et ne sont plus pris en compte dans le calcul de contradiction. Sont visibles les zones qui sont contradictoires à toute heure de la nuit, nécessitant une attention partculière.
* Différence : seuls les magasins et la biodiversité sont pris en compte dans la valeur de contradiction. Sont visibles les zones où l'usage citoyen décroit fortement dans la nuit, il peut être fortement intéressant de réduire l'intensité des luminaires de ces zones afin de respecter au mieux la biodiversité à proximité.
L'addition des calques Nuit + Différence est équivalent au calque Jour.

"""

DESC3 = """
Cette carte permet de visualiser l'impact des luminaires sur la biodiversité locale.
Pollux affecte à chaque luminaire une valeur d'impact, qui dépend essentiellement de deux facteurs :
* La proximité de l'objet avec la source lumineuse
* La quantité d'objets éclairés par la source lumineuse

Cette valeur est traduite sur une échelle de couleur allant du rouge (niveau élevé) au violet (niveau faible).

Les luminaires peuvent posséder une température de couleur (K) basse (compatible avec la biodiversité) ou posséder plusieurs régimes : leur intensité lumineuse varie selon l'heure de la nuit.
Pour représenter cet élément, deux filtres sont disponibles :
* Jour (ou début de soirée) : sont retirés les luminaires ayant une température de couleur inférieure ou égale à 2500K, ainsi que ceux fonctionnant avec des détecteurs de présence.
* Nuit : c'est le calque Jour avec un filtre supplémentaire : sont également retirés les luminaires présentant une baisse de leur intensité au cours de la nuit."""