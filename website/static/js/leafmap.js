let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.188848, 5.707703]]);
let baseClickableZone = createRectangle(clickZoneBound, color='yellow');
var baseLayer = new L.FeatureGroup([baseClickableZone]);
var editableLayer = new L.FeatureGroup();

var tempForm = null;
var blockTempForm = false;
var defaultCircleRadius = 10;

var fileAndName = [
                        {'filename': 'trees_output.json',
                         'entityName': 'Arbres',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'crossings_output.json',
                         'entityName': 'Passages piétons',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'accidents_2019_2020_output.json',
                         'entityName': 'Accidents de voiture de nuit',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'tc_ways_output.json',
                         'entityName': 'Lignes de bus',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'tc_stops_output.json',
                         'entityName': 'Arrêts de transports en commun',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'parks_output.json',
                         'entityName': 'Parcs',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'birds_output.json',
                         'entityName': 'Observations oiseau',
                         'data': {},
                         'layer': new L.FeatureGroup()},
                      ];

loadJsons()


function loadJsons() {
    for (linkFileName of fileAndName) {
        loadJson(linkFileName)
    }
}

var controlLayers = {
    "Base": baseLayer,
    "Mon Calque": editableLayer,
};

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
        layers: [baseLayer, editableLayer],
    }).setView(clickZoneBound.getCenter(), 17);


for (dict_data of fileAndName) {
    controlLayers[dict_data.entityName] = dict_data.layer
}

L.control.layers(null, controlLayers).addTo(map);

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
    //polygon: false,
    marker: false,
    },
  edit: {
    featureGroup: editableLayer,
    remove: true
  }
};


// Active control buttons
var drawControl = new L.Control.Draw(drawPluginOptions);
map.addControl(drawControl);


function createTooltipContent(layer) {
    let tooltipContent = '';
    let surface = 0;

    if (layer instanceof L.CircleMarker) { // include Circle
        for (data_dict of fileAndName) {
            tooltipContent += '<b>' + data_dict.entityName + '</b>' +
                              ': ' +
                              nbObjInRange(data_dict.data.features, layer.getLatLng(), layer.getRadius()) +
                              '<br/>';
        }
        surface = layer.getRadius()*layer.getRadius()*3.141592654;
    } else if (layer instanceof L.Polygon) { // include Rectangle
        for (data_dict of fileAndName) {
            tooltipContent += '<b>' + data_dict.entityName + '</b>' +
                              ': ' +
                              nbObjInBound(data_dict.data.features, layer.getBounds()) +
                              '<br/>';
        }
        surface = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
    }
    layer.bindTooltip(tooltipContent)
}


// temporary circle with simple click
map.on('click', function(e) {
    if (!blockTempForm & clickZoneBound.contains(e.latlng)) {
        if (tempForm !== null) {
            editableLayer.removeLayer(tempForm);
            map.removeLayer(tempForm);
        }
        tempForm = createCircle(e.latlng, radius=defaultCircleRadius).addTo(map);
        createTooltipContent(tempForm);
        editableLayer.addLayer(tempForm);
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
    editableLayer.addLayer(layer);
});


// tooltip update
map.on('draw:edited', function(e) {
    for (var layer of Object.values(e.layers._layers)) {
        createTooltipContent(layer);
    }
});


function reverse_polygon_pos(coordinates) {
    let ret = [[]];
    for (lines of coordinates) {
        for (position of lines) {
            ret[0].push(position.slice().reverse())
        }
    }
    return ret
}


function nbObjInRange(features, ePosition, radius) {
    let nbObj = 0;
    features.forEach(function(d) {
        if (d.geometry.type == 'Point') {
            nbObj += map.distance(ePosition, d.geometry.coordinates.slice().reverse()) <= radius ? 1 : 0
        } else if (d.geometry.type == 'MultiLineString' || d.geometry.type == 'Polygon') {
            if (d.geometry.type == 'Polygon' &
                L.latLngBounds(reverse_polygon_pos(d.geometry.coordinates)).contains(ePosition)) {
                    nbObj += 1
            } else {
                for (lines of d.geometry.coordinates) {
                    for (position of lines) {
                        if (ePosition.distanceTo(position.slice().reverse()) <= radius) {
                            nbObj += 1
                            break
                            break
                        }
                    }
                }
            }
        }
    });
    return nbObj
}


function nbObjInBound(features, bound) {
    let nbObj = 0;
    features.forEach(function(d) {
        if (d.geometry.type == 'Point') {
            nbObj += bound.contains(d.geometry.coordinates.slice().reverse()) ? 1 : 0
        } else if (d.geometry.type == 'MultiLineString' || d.geometry.type == 'Polygon') {
            if (d.geometry.type == 'Polygon' &
                L.latLngBounds(reverse_polygon_pos(d.geometry.coordinates)).intersects(bound)) {
                    nbObj += 1
            } else {
                for (lines of d.geometry.coordinates) {
                    for (position of lines) {
                        if (bound.contains(position.slice().reverse())) {
                            nbObj += 1
                            break
                            break
                        }
                    }
                }
            }
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