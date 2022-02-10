let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.188848, 5.707703]]);
var layerBase = L.layerGroup([L.marker(clickZoneBound.getCenter())]);
var editableLayers = new L.FeatureGroup();

var map = L.map('city_map', {
        layers: [layerBase, editableLayers],
    }).setView(clickZoneBound.getCenter(), 17);

var overlayMaps = {
    "Base": layerBase,
    "Mon Calque": editableLayers,
};
L.control.layers(null, overlayMaps).addTo(map);

// Test area
createRectangle(clickZoneBound, color='yellow').addTo(map);

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);


var tempForm = null;
var circleRadius = 10;

var fileAndName = [
                        ['trees_output.json', 'Arbres'],
                        ['crossings_output.json', 'Passages piétons'],
                      ];

loadJsons()


function loadJsons() {
    for (linkFileName of fileAndName) {
        loadJson(linkFileName)
    }
}


function loadJson(linkFileName) {
    let request = new Request('/api/' + linkFileName[0], {
        method: 'GET',
        headers: new Headers(),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        linkFileName.push(data);
        //L.geoJSON(data).addTo(map);
    });
}


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
        radius: radius || circleRadius,
    })
}


var drawPluginOptions = {
  draw: {
    rectangle: {
      shapeOptions: {
        color: '#97009c'
      }
    },
    circle: {
      shapeOptions: {
        color: '#b7000c'
      }
    },

    polyline: false,
    polygon: false,
    marker: false,
    },
  edit: {
    featureGroup: editableLayers,
    remove: true
  }
};


// Initialise the draw control and pass it the FeatureGroup of editable layers
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);


function createTooltipContent(layer) {
    var tooltipContent = '';
    for ([filename, entityName, data] of fileAndName) {
        let nbObj = 0;

        if (layer instanceof L.CircleMarker) { // include Circle
            nbObj += nbObjInRange(map, data, layer.getLatLng(), layer.getRadius());
        } else if (layer instanceof L.Polygon) { // include Rectangle
            nbObj += nbObjInBound(data, layer.getBounds());
        }

        tooltipContent += '<br/>' + entityName + ': ' + nbObj;
      }

    layer.bindTooltip(tooltipContent)
    }


// temporary circle with simple click
map.on('click', function(e) {
    if (tempForm !== null) {
        editableLayers.removeLayer(tempForm);
    }
    tempForm = createCircle(e.latlng, radius=circleRadius).addTo(map);
    createTooltipContent(tempForm);
    editableLayers.addLayer(tempForm);
});


// create form
map.on('draw:created', function(e) {
    var layer = e.layer;
    createTooltipContent(layer);
    editableLayers.addLayer(layer);
});


// tooltip update
map.on('draw:edited', function(e) {
    for (var layer of Object.values(e.layers._layers)) {
        createTooltipContent(layer);
    }
});
