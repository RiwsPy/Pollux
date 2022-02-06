let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.188848, 5.707703]]);
var map = L.map('city_map').setView(clickZoneBound.getCenter(), 17);
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);

create_rectangle(clickZoneBound, color='yellow').addTo(map);

var popup = L.popup();
var circle = null;
var rectangle = null;
var positionClick1 = null;
var position_popup = null;
var nbObj = 0;
var circle_radius = 10;
var txt_content = '';

var fileAndName = [
                        ['trees_output.json', 'Arbres'],
                        ['crossings_output.json', 'Passages piétons'],
                      ];
load_jsons()

function load_jsons() {
    for (index in fileAndName) {
        load_json(index)
    }
}

function load_json(index) {
    let request = new Request('/api/' + fileAndName[index][0], {
        method: 'GET',
        headers: new Headers(),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        fileAndName[index].push(data)
    });
}

function onMapClick(e) {
    if (circle !== null) {
        map.removeLayer(circle);
    }
    if (rectangle !== null) {
        map.removeLayer(rectangle);
    }
    if (e.originalEvent.ctrlKey) {
        if (positionClick1 == null) {
            positionClick1 = e.latlng
            return null
    }}

    txt_content = 'Coordonnées ' + e.latlng.toString() + '<br/>';

    if (e.originalEvent.ctrlKey) { // second click
        bound = L.latLngBounds([e.latlng, positionClick1]);
        rectangle = create_rectangle(bound).addTo(map);
        position_popup = L.latLng(bound.getNorth(), (bound.getEast()+bound.getWest())/2);
        //map.fitBounds(bound);

    } else { // Click without ctrl
        circle = create_circle(e.latlng, radius=circle_radius).addTo(map);
        position_popup = L.latLng(e.latlng.lat+circle_radius/100000, e.latlng.lng);
    }

    for (file_and_name of fileAndName) {
        let entityName = file_and_name[1];
        let data = file_and_name[2];

        if (e.originalEvent.ctrlKey) { // second click
            nbObj = nbObjInBound(data, bound);
        } else { // Click without ctrl
            nbObj = nbObjInRange(map, data, e.latlng, circle_radius);
        }

        positionClick1 = null;
        txt_content += '<br/>' + entityName + ': ' + nbObj;
      }

    popup
        .setLatLng(position_popup)
        .setContent(txt_content)
        .openOn(map);
    }
    //data.txt_content += "<br/><br/>" +
    //    "<a href='' target='blank'>Signaler</a> un problème à cet endroit.";


map.on('click', onMapClick);


function nbObjInRange(map, data, ePosition, radius) {
    var nbObj = 0;
    data.features.forEach(function(d) {
        if (map.distance(ePosition, d.geometry.coordinates.reverse()) <= radius) {
            nbObj += 1
        }
    });
    return nbObj
}

function nbObjInBound(data, bound) {
    var nbObj = 0;
    data.features.forEach(function(d) {
        if (bound.contains(d.geometry.coordinates.reverse())) {
            nbObj += 1
        }
    });
    return nbObj
}

function create_rectangle(bound, color, fillColor, fillOpacity) {
    return L.rectangle(bound, {
        color: color || 'green',
        fillColor: fillColor || '#3c0',
        fillOpacity: fillOpacity || 0.1,
    })
}

function create_circle(ePosition, color, fillColor, fillOpacity, radius) {
    return L.circle(ePosition, {
        color: color || 'red',
        fillColor: fillColor || '#f03',
        fillOpacity: fillOpacity || 0.5,
        radius: radius || 10,
    })
}