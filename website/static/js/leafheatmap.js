let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.198848, 5.725703]]);
let baseClickableZone = createRectangle(clickZoneBound, color='yellow');
var baseLayer = new L.FeatureGroup([baseClickableZone]);

var fileAndName = [
                        {'filename': 'trees_output.json',
                         'entityName': 'Arbres',
                         'entityClipsName': 'Tree',
                         'data': {},
                         'heatColor': 'red',
                         'layer': new L.FeatureGroup()},

                        {'filename': 'crossings_output.json',
                         'entityName': 'Passages piétons',
                         'entityClipsName': 'Crossing',
                         'data': {},
                         'heatColor': 'blue',
                         'layer': new L.FeatureGroup()},

                        {'filename': 'accidents_2019_2020_output.json',
                         'entityName': 'Accidents de voiture de nuit',
                         'entityClipsName': 'Accident',
                         'data': {},
                         'heatColor': 'blue',
                         'layer': new L.FeatureGroup()},

                        {'filename': 'tc_stops_output.json',
                         'entityName': 'Arrêts de transports en commun',
                         'entityClipsName': 'PublicTransportStop',
                         'data': {},
                         'heatColor': 'blue',
                         'layer': new L.FeatureGroup()},

                        {'filename': 'birds_output.json',
                         'entityName': 'Observations oiseau',
                         'entityClipsName': 'Animal',
                         'data': {},
                         'heatColor': 'red',
                         'layer': new L.FeatureGroup()},

                        {'filename': 'shops_output.json',
                         'entityName': 'Bâtiments accueillant du public',
                         'entityClipsName': 'Shop',
                         'data': {},
                         'heatColor': 'blue',
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
        let heatMapData = [];
        data.features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                heatMapData.push([
                    +d.geometry.coordinates[1],
                    +d.geometry.coordinates[0],
                    1.0]);
            }
        });
        let gradientColor = {};
        if (linkFileName.heatColor == 'red') {
            gradientColor = {
                    0.00: 'yellow',
                    0.50: 'orange',
                    1.0: 'red'}
        } else if (linkFileName.heatColor == 'blue') {
            gradientColor = {
                    0.00: 'green',
                    0.50: 'blue',
                    1.0: 'violet'}
        }

        L.heatLayer(heatMapData, {
            maxZoom: 17,
            radius: 50,
            max: 1.0,
            blur: 0,
            gradient: gradientColor}).addTo(linkFileName.layer);
    });
}

var map = L.map('city_map', {
        layers: [baseLayer],
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


// Active control buttons
map.addControl(new L.Control.Fullscreen({
    title: {
        'false': 'Vue plein écran',
        'true': 'Quitter le plein écran'
    }
}));


function createRectangle(bound, color, fillColor, fillOpacity) {
    return L.rectangle(bound, {
        color: color || 'green',
        fillColor: fillColor || '#3c0',
        fillOpacity: fillOpacity || 0.1,
    })
}

// basic leaflet traduction
document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';

