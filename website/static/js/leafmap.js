let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.198848, 5.725703]]);
let baseClickableZone = createRectangle(clickZoneBound, color='yellow');
var baseLayer = new L.FeatureGroup([baseClickableZone]);
var editableLayer = new L.FeatureGroup();

var tempForm = null;
var blockTempForm = false;
var defaultCircleRadius = 10;

var recommendationContent = document.getElementById("clips_recommendations_content");

var fileAndName = [
                        {'filename': 'trees_output.json',
                         'entityName': 'Arbres',
                         'entityClipsName': 'Tree',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'crossings_output.json',
                         'entityName': 'Passages piétons',
                         'entityClipsName': 'Crossing',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'accidents_2019_2020_output.json',
                         'entityName': 'Accidents de voiture de nuit',
                         'entityClipsName': 'Accident',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'tc_ways_output.json',
                         'entityName': 'Lignes de bus',
                         'entityClipsName': 'BusLine',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'tc_stops_output.json',
                         'entityName': 'Arrêts de transports en commun',
                         'entityClipsName': 'PublicTransportStop',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'parks_output.json',
                         'entityName': 'Parcs',
                         'entityClipsName': 'Park',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'birds_output.json',
                         'entityName': 'Observations oiseau',
                         'entityClipsName': 'Animal',
                         'data': {},
                         'layer': new L.FeatureGroup()},

                        {'filename': 'shops_output.json',
                         'entityName': 'Bâtiments accueillant du public',
                         'entityClipsName': 'Shop',
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
        L.geoJSON(data).addTo(linkFileName.layer);
    });
}

var map = L.map('city_map', {
        layers: [baseLayer, editableLayer],
        minZoom: 15,
        maxBounds: clickZoneBound,
        //fullscreenControl: true,
    }).setView(clickZoneBound.getCenter(), 16);

for (dict_data of fileAndName) {
    controlLayers[dict_data.entityName] = dict_data.layer
}

L.control.layers(null, controlLayers).addTo(map);

//const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
L.tileLayer('https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(map);
//L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', { attribution: attribution }).addTo(map);

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
    featureGroup: editableLayer,
    remove: true
  }
};


// Active control buttons
map.addControl(new L.Control.Fullscreen({
    title: {
        'false': 'Vue plein écran',
        'true': 'Quitter le plein écran'
    }
}));

map.addControl(new L.Control.Draw(drawPluginOptions));

function createTooltipContent(layer) {
    let tooltipContent = '';
    var requestClips = {
        hasArea: 0.0,
        latLng: {lat: 0.0, lng: 0.0},
        schedule: '2023-02-01 08:00',
        InfluencingElements: [],
    }

    if (layer instanceof L.CircleMarker) { // include Circle
        for (data_dict of fileAndName) {
            requestClips.InfluencingElements.push(...nbObjInRangeClips(data_dict, layer.getLatLng(), layer.getRadius()))
            tooltipContent += '<b>' + data_dict.entityName + '</b>' +
                              ': ' +
                              nbObjInRange(data_dict.data.features, layer.getLatLng(), layer.getRadius()) +
                              '<br/>';
        }
        requestClips.hasArea = layer.getRadius()*layer.getRadius()*3.141592654;
        requestClips.latLng = layer.getLatLng();
    } else if (layer instanceof L.Polygon) { // include Rectangle
        for (data_dict of fileAndName) {
            requestClips.InfluencingElements.push(...nbObjInBoundClips(data_dict, layer.getBounds()))
            tooltipContent += '<b>' + data_dict.entityName + '</b>' +
                              ': ' +
                              nbObjInBound(data_dict.data.features, layer.getBounds()) +
                              '<br/>';
        }
        requestClips.hasArea = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
        requestClips.latLng = layer.getBounds().getCenter();
    }
    layer.bindTooltip(tooltipContent)

    let request = new Request('/clips/', {
        method: 'POST',
        headers: new Headers(),
        body: JSON.stringify(requestClips),
        })

    console.log(JSON.stringify(requestClips))
    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        //layer.bindTooltip(data.recommendation);
        recommendationContent.innerHTML = data.recommendation;
    });
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

function nbObjInRangeClips(features, ePosition, radius) {
    let requestClips = []
    features.data.features.forEach(function(d) {
        if (d.geometry.type == 'Point') {
            if (map.distance(ePosition, d.geometry.coordinates.slice().reverse()) <= radius) {
                requestClips.push(generateClipsContent(d, features.entityClipsName))
            }
        } else if (d.geometry.type == 'MultiLineString' || d.geometry.type == 'Polygon') {
            if (d.geometry.type == 'Polygon' &
                L.latLngBounds(reverse_polygon_pos(d.geometry.coordinates)).contains(ePosition)) {
                    requestClips.push(generateClipsContent(d, features.entityClipsName))
            } else {
                for (lines of d.geometry.coordinates) {
                    for (position of lines) {
                        if (ePosition.distanceTo(position.slice().reverse()) <= radius) {
                            requestClips.push(generateClipsContent(d, features.entityClipsName))
                            break
                            break
                        }
                    }
                }
            }
        }
    });
    return requestClips
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

function nbObjInBoundClips(features, bound) {
    let requestClips = [];
    features.data.features.forEach(function(d) {
        if (d.geometry.type == 'Point') {
            if (bound.contains(d.geometry.coordinates.slice().reverse())) {
                requestClips.push(generateClipsContent(d, features.entityClipsName))
            }
        } else if (d.geometry.type == 'MultiLineString' || d.geometry.type == 'Polygon') {
            if (d.geometry.type == 'Polygon' &
                L.latLngBounds(reverse_polygon_pos(d.geometry.coordinates)).intersects(bound)) {
                    requestClips.push(generateClipsContent(d, features.entityClipsName))
            } else {
                for (lines of d.geometry.coordinates) {
                    for (position of lines) {
                        if (bound.contains(position.slice().reverse())) {
                            requestClips.push(generateClipsContent(d, features.entityClipsName))
                            break
                            break
                        }
                    }
                }
            }
        }
    });
    return requestClips
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
    } else if (category_name == 'PublicTransportStop' || category_name == 'BusLine') {
        ret.openingHours = 'Mo-Su 05:00-24:00'
    }
    return ret
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


// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';

