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
        content += addNewLineInContent('Période', properties["Lampe - Régime (simplifié)"])
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
