DESC1 = """

Sur cette carte vous êtes invités à créer votre propre zone géographique d'analyse.
Celle-ci peut couvrir un quartier, une rue ou même le devant de sa porte.
Une fois fait, Pollux identifie les différents éléments présents dans cette zone ayant un impact sur la politique d'éclairage public.
Cela peut être un parc, un passage piétonnier, un arrêt de bus...
<hr class="divider">

<strong>A quoi sert la zone de droite ?</strong>

Dans le panneau latéral droit, s'affichera les recommandations d'éclairage en fonction des éléments présents dans la zone que vous avez créé.
Ces recommandations sont issues des normes en vigueur ou bien d'associations engagées dans le domaine de l'éclairage public.

Certains termes peuvent être techniques alors n'hésitez pas à consulter notre <a href="/encyclopedia" target="_blank" class="invisible_link">encyclopédie<img src="../static/img/buttons/encyclopedie.png" width="40"></a>
<hr class="divider">

<strong>Comment je crée une zone ?</strong>

La façon la plus élémentaire : c'est de cliquer sur la carte.
Un simple clic crée un cercle rouge d'un rayon de 10 mètres.

<img src="../static/img/button_dessin.png"> Il est possible de créer d'autres formes grâce à la barre de dessin. Essayez-les !
<hr class="divider">

<strong>Comment je modifie une zone ?</strong>

Il est possible de déplacer, de modifier et de supprimer les formes créées.
<img src="../static/img/button_trash.png"> Il suffit de cliquer sur le bouton adéquat puis de cliquer sur la zone que vous souhaitez modifier.
Une fois terminé, n'oubliez pas de cliquer sur le bouton <img src="../static/img/button_save.png"> !
<hr class="divider">

<strong>Comment j'affiche les éléments dans une zone ?</strong>

Tout d'abord, en passant votre souris sur la forme créée, s'affichera le nombre des différents éléments trouvés.

Pour plus de détails, vous trouverez en haut à droite le bouton Calque. <img src="../static/img/button_calque.png">
En cliquant sur le ou les calques qui vous intéresse(nt) vous afficherez les éléments que vous désirez.

Deux calques particuliers sont présents :
<li><b>Zone Test</b> : affiche ou cache les limites de la zone couverte par Pollux, au-delà, c'est le vide !
<li><b>Mon Calque</b> : affiche ou cache les différentes formes que vous avez créé.
<hr class="divider">

<strong>Et si je veux encore plus d'information sur les éléments affichés ?</strong>

Après avoir coché le calque correspondant aux éléments recherchés, il est possible de cliquer individuellement sur ces éléments.
Diverses informations sont renseignées comme par exemple l'espèce de l'arbre ou les horaires d'ouvertures du magasin.
<hr class="divider">

<strong>Et si je veux en savoir encore plus ?</strong>

Nous vous invitons à regarder la vidéo explicative en début de page. Bon visionnage !
"""

DESC2 = """

L'objectif de la carte de contradiction est d'identifier les zones où sont présents des éléments dont les impacts sur la politique d'éclairage sont opposés.
<hr class="divider">

<strong>Des éléments opposés ? C'est-à-dire ?</strong>

Ici, les besoins des passages piétons et les magasins sont opposés à la biodiversité.
En effet, les passages piétons représentent une zone d'insécurité où une forte intensité lumineuse et un excellent rendu des couleurs sont attendus.
Quant aux magasins, ils attirent les citoyens ce qui génère des zones à fort besoin lumineux, notamment pour le confort et l'impression de sécurité que la lumière apporte.

Pour ces deux raisons, l'éclairage public privilégie une luminosité <u>élevée</u> et une température de couleur <u>froide</u>.
En contradiction avec la biodiversité, qui préfère une luminosité <u>faible</u> et une température de couleur <u>chaude</u>.
<hr class="divider">

<strong>Que faîtes-vous une fois ces zones de contradictions identifiées ?</strong>

Pour chacune d'entre elles, Pollux leur affecte une valeur en fonction de la densité des éléments identifiés comme contradictoires et de la distance les séparant.

Cette valeur est traduite sur une échelle de couleur allant du <span style="color: red;">rouge (niveau élevé)</span> au <span style="color: violet;">violet (niveau faible)</span>.
<hr class="divider">

<strong>A quelle valeur correspond la couleur rouge ou la couleur violette ?</strong>

La valeur des couleurs est détaillée dans la légende mais une couleur ne correspond pas à une valeur fixe.
Il nous faut rappeler que la carte est interactive : il est possible de zoomer et de dézoomer.
Dans ce cas, appliquer une échelle de valeur fixe à une carte évolutive n'est pas efficace : la carte ne serait exploitable que sur une tranche de zoom très limitée.
Afin de remédier à cela, nous avons opté pour une échelle aussi flexible que la carte !
<hr class="divider">

<strong>A quoi correspondent les calques ?</strong>

Sur cette carte, <b>3 calques sont disponibles</b> :
<ol><div>
<li><strong>Jour</strong> : qui indique les zones de contradiction en début de soirée.</i>
<li><strong>Nuit</strong> : qui indique les zones qui sont contradictoires à toute heure de la nuit et donc nécessitant une attention particulière.</i>
<li><strong>Différence</strong> : qui indique les zones où le besoin d'éclairage décroit fortement dans la nuit, il est intéressant de réduire l'intensité lumineuse au cours de la nuit des points lumineux dans ces zones afin de respecter au mieux la biodiversité à proximité.</i>
</div></ol>
"""

DESC3 = """

Cette carte permet de visualiser l'impact des luminaires sur la biodiversité locale.
<hr class="divider">

<strong>Comment est calculé l'impact des luminaires ?</strong>

Pollux affecte à chaque luminaire une première valeur d'impact, qui dépend de deux facteurs :
<li>La quantité d'objets éclairés par la source lumineuse</li>
<li>La distance entre l'ampoule et l'objet éclairé</li>
<hr class="divider">

<strong>Pourquoi parler d'une distance de l'ampoule plutôt que du luminaire ?</strong>

Pour le calcul d'impact, la distance est un facteur clé.
Car <u>multiplier la distance par 2, c'est diviser l'impact par 4</u>.
Pour cette raison, la valeur de la distance doit être aussi précise que possible.
Dans ce cas, la géolocalisation des objets est nécessaire mais insuffisante.

Prenons un exemple :
Je me place sous un luminaire, quelle distance nous sépare ?
En théorie, nous sommes à la même position, donc <u>la distance est nulle</u>.
Ce raisonnement est correct sauf que ce n'est pas le luminaire qui m'éclaire mais son ampoule !

Ainsi en restant sous le luminaire, si je mesure 1m80 et le luminaire 8 mètres, <u>la distance devient 6m20</u>.
L'impact n'est plus le même.

De plus, cette valeur sert de base pour les calculs suivants.
En effet, plusieurs données permettent d'affiner ce premier résultat.
<hr class="divider">

<strong>Quelles sont les autres données impactantes ?</strong>

<b>1.</b> La température de couleur de l'ampoule
Nous considérons qu'une température inférieure à 2500 Kelvins possède un impact faible sur la biodiversité.
<b>2.</b> La détection de présence
Nous considérons également que les luminaires fonctionnant par détection possèdent un impact faible, du fait de leur faible durée d'éclairage.
<b>3.</b> Le type de régime
Il est courant que les luminaires possèdent deux plages de fonctionnement :
la première pour la soirée et le matin, la seconde pour la nuit.
Pour prendre en compte ce dernier paramètre, deux calques sont disponibles : <b>Jour</b> et <b>Nuit</b>.
Un luminaire dont le flux lumineux est réduit de 50% pendant la nuit, voit son impact réduit de 50% sur le calque Nuit.

Enfin, cette valeur d'impact est traduite sur une échelle de couleur allant du <span style="color: red;">rouge (niveau élevé)</span> au <span style="color: violet;">violet (niveau faible)</span>.
<hr class="divider">

<strong>A quoi sert le calque <i>Luminaires</i> ?</strong>

A la différence de la <a href="/map_desc/2" target="_blank" class="invisible_link">carte de Contradiction</a> qui signale des zones, celle-ci éclaire les luminaires - un comble pour eux.
C'est-à-dire que chaque point correspond exactement à un luminaire.
Avec les calques Jour et Nuit, il était possible d'identifier les positions des luminaires à fort impact.
Mais en rajoutant le calque Luminaire, Pollux va plus loin.
Car il permet également à l'utilisateur d'accéder aux caractéristiques du luminaire sur lequel il clique.
"""
