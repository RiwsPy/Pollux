let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.188848, 5.707703]]);
var baseLayer = L.layerGroup([L.marker(clickZoneBound.getCenter())]);
var editableLayers = new L.FeatureGroup();
var treeLayer = new L.FeatureGroup();
var crossingLayer = new L.FeatureGroup();

var tempForm = null;
var blockTempForm = false;
var defaultCircleRadius = 10;

var fileAndName = [
                        {'filename': 'trees_output.json',
                         'entityName': 'Arbres',
                         'data': {},
                         'layer': treeLayer},

                        {'filename': 'crossings_output.json',
                         'entityName': 'Passages piétons',
                         'data': {},
                         'layer': crossingLayer},
                      ];

loadJsons()


function loadJsons() {
    for (linkFileName of fileAndName) {
        loadJson(linkFileName)
    }
}


function loadJson(linkFileName) {
    let request = new Request('/api/' + linkFileName.filename, {
        method: 'GET',
        headers: new Headers(),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        linkFileName.data = data;
        //L.geoJSON(data).addTo(linkFileName.layer);
    });
}


var map = L.map('city_map', {
        layers: [baseLayer, editableLayers],
    }).setView(clickZoneBound.getCenter(), 17);


var overlayMaps = {
    "Base": baseLayer,
    "Mon Calque": editableLayers,
};

for (dict_data of fileAndName) {
    overlayMaps[dict_data.entityName] = dict_data.layer
}

L.control.layers(null, overlayMaps).addTo(map);

// Test area
createRectangle(clickZoneBound, color='yellow').addTo(map);

const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: attribution }).addTo(map);

var drawPluginOptions = {
  draw: {
    rectangle: {
      shapeOptions: {
        color: '#97009c'
      },
      //repeatMode: true,
    },
    circle: {
      shapeOptions: {
        color: '#b7000c'
      },
      //repeatMode: true,
    },
    polygon: {
      shapeOptions: {
        color: '#07b90c'
      },
      //repeatMode: true,
    },
    circlemarker: {
      //repeatMode: true,
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


// Active control buttons
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);


function createTooltipContent(layer) {
    var tooltipContent = '';
    for (data_dict of fileAndName) {
        let nbObj = 0;

        if (layer instanceof L.CircleMarker) { // include Circle
            nbObj += nbObjInRange(map, data_dict.data, layer.getLatLng(), layer.getRadius());
        } else if (layer instanceof L.Polygon) { // include Rectangle
            nbObj += nbObjInBound(data_dict.data, layer.getBounds());
        }

        tooltipContent += data_dict.entityName + ': ' + nbObj + '<br/>';
    }
    layer.bindTooltip(tooltipContent)
}


// temporary circle with simple click
map.on('click', function(e) {
    if (blockTempForm == false) {
        if (tempForm !== null) {
            editableLayers.removeLayer(tempForm);
            map.removeLayer(tempForm);
        }
        tempForm = createCircle(e.latlng, radius=defaultCircleRadius).addTo(map);
        createTooltipContent(tempForm);
        editableLayers.addLayer(tempForm);
    }
});


// lock default click if a new form is drawing
map.on('draw:drawstart', function(e) {
    lockTempForm();
})
map.on('draw:deletestart', function(e) {
    lockTempForm();
})

// unlock
map.on('draw:drawstop', function(e) {
    unlockTempForm();
})
map.on('draw:deletestop', function(e) {
    unlockTempForm();
})

function lockTempForm() {
    blockTempForm = true;
}

function unlockTempForm() {
    blockTempForm = false;
}


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
        radius: radius || defaultCircleRadius,
    })
}