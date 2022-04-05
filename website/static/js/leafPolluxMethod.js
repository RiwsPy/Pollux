function defaultZonePos() {
    return [[45.187501, 5.704696], [45.198848, 5.725703]];
}

function defaultZoneBound() {
    return L.latLngBounds(defaultZonePos());
}

function addAttribution(map, mapName) {
    /*
    if (mapName == 'Impact') {
        let tileLayer = L.tileLayer('//{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
            maxZoom: 20,
            attribution: 'donn&eacute;es &copy; <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
            }).addTo(map);
    } else {*/
    let tileLayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
        maxZoom: 20,
        attribution: '<a href="https://green-pollux.herokuapp.com">Pollux ' + mapName + '</a>, &copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
        }).addTo(map);
    //}
}

function addPopUp(feature, layer, categoryName) {
    if (feature.properties) {
        layer.bindPopup(generatePupUpContent(feature.properties, categoryName) || 'Test');
    }
}

function getIcon(feature) {
    return L.icon({
        iconUrl: '../static/img/' + feature.icon,
        iconSize: [20, 20],
        });
}

function generateClipsContent(obj, category_name) {
    let ret = {type: category_name}
    if (category_name === 'Tree') {
        ret.genre = obj.properties.GENRE_BOTA
        ret.species = obj.properties.ESPECE
    } else if (category_name == 'Shop') {
        ret.openingHours = obj.properties.opening_hours
        ret.name = obj.properties.name
    } else if (category_name == 'Animal') {
        ret.species = obj.properties.NomCite
        ret.speciesScient = obj.properties.NomScientifiqueRef
        ret.sensible = obj.properties.Sensible
    } else if (category_name == 'BusLine') {
        ret.openingHours = 'Mo-Su 05:00-24:00'
        ret.name = obj.properties.LIBELLE
        ret.line_number = obj.properties.NUMERO
    } else if (category_name == 'PublicTransportStop') {
        ret.openingHours = 'Mo-Su 05:00-24:00'
        ret.name = obj.properties.name
    }
    return ret
}


function generatePupUpContent(properties, categoryName) {
    let content = '';
    if (categoryName == 'Park') {
        content += (properties.name || '') + '<br>'
    } else if (categoryName == 'Tree') {
        content += addNewLineInContent('Arbre', properties.ESPECE)
        if (properties.ANNEEDEPLANTATION) {
            content += addNewLineInContent('Année de plantation', properties.ANNEEDEPLANTATION)
        }
    } else if (categoryName == 'BusLine') {
        content += addNewLineInContent('Ligne de bus', properties.NUMERO)
    } else if (categoryName == 'Animal') {
        content += addNewLineInContent('Espèce', properties.NomVernaculaire)
    } else if (categoryName == 'Lamp') {
        content += addNewLineInContent('Luminaire n°', properties['Luminaire - Code luminaire'])
        content += addNewLineInContent('Température (K)', properties["Lampe - Température Couleur"])
        content += addNewLineInContent('Rendu couleur (%)', properties["Lampe - IRC"])
        content += addNewLineInContent('Régime', properties["Lampe - Régime (simplifié)"])
        content += addNewLineInContent('Hauteur (m)', properties["Luminaire - Hauteur de feu"])
    } else if (categoryName == 'Shop') {
        content += addNewLineInContent('', properties.name)
        content += addNewLineInContent("Horaires d'ouvertures", properties.opening_hours)
    }
    return content //+ '<br>+ recommandations connues'
}


function addNewLineInContent(category, content) {
    return '<b>' + category + '</b> ' + (content || '') + '<br>'
}


function createRectangle(bound, color, fillColor, fillOpacity) {
    return L.rectangle(bound, {
        color: color || 'green',
        fillColor: fillColor || '#3c0',
        fillOpacity: fillOpacity || 0.1,
    })
}


function createCircle(ePosition, color, fillColor, fillOpacity, radius) {
    return L.circle(ePosition, {
        color: color || 'red',
        fillColor: fillColor || '#f03',
        fillOpacity: fillOpacity || 0.5,
        radius: radius || defaultCircleRadius,
    })
}


function addDescButton(map) {
    let url = new URL(window.location.href)
    let url_split = url.pathname.split('/')
    let map_id = url_split[2]
    let htmlValue = '<a id="mapButton" href="/map_desc/' + map_id + '" title="Ouvrir la description" target="_blank"><i style="width: 17px;" class="fa fa-book fa-lg"></i></a>'
    addButton(map, htmlValue)
}


function addHomeButton(map) {
    addButton(map,
              '<a id="mapButton" href="/" title="Retour à l\'accueil"><i style="width: 17px;" class="fas fa-door-open"></i></a>'
             )
}


function addButton(map, htmlValue) {
    let homeButton = L.control({ position: "topleft" });
    homeButton.onAdd = function(map) {
        let div = L.DomUtil.create("div");
        div.innerHTML += htmlValue
        return div;
    };
    homeButton.addTo(map);
}

function reverse_polygon_pos(coordinates) {
    let ret = [[]];
    for (lines of coordinates) {
        for (position of lines) {
            ret[0].push(position.slice().reverse())
        }
    }
    return ret
}