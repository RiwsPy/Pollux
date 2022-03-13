let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.198848, 5.725703]]);
let baseClickableZone = createRectangle(clickZoneBound, color='yellow');
var baseLayer = new L.FeatureGroup([baseClickableZone]);
var editableLayer = new L.FeatureGroup();

var fileLayer = [
    {
        filename: 'conflict_lamps__trees.json',
        layername: 'Jour',
        layer: new L.FeatureGroup(),
    },
    {
        filename: 'conflict_lamps_night__trees.json',
        layername: 'Nuit',
        layer: new L.FeatureGroup(),
    },
]

var controlLayers = {
    "Base": baseLayer,
};
for (fileData of fileLayer) {
    controlLayers[fileData.layername] = fileData.layer}


var map = L.map('city_map', {
        layers: [baseLayer, fileLayer[0].layer],
        minZoom: 15,
        //maxBounds: clickZoneBound,
        //fullscreenControl: true,
    }).setView(clickZoneBound.getCenter(), 16);

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

loadJsons()

function loadJsons() {
    for (fileData of fileLayer) {
        loadJson(fileData)
    }
}

function loadJson(fileData) {
    let request = new Request('/api/' + fileData.filename, {
        method: 'GET',
        headers: new Headers(),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        //linkFileName.data = data;
        //L.geoJSON(data).addTo(linkFileName.layer);
        let heatMapData = [];
        data.features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                heatMapData.push([
                    +d.geometry.coordinates[0],
                    +d.geometry.coordinates[1],
                    +d.properties.intensity]);
            }
        });

        gradientColor = {
                0.0: 'violet',
                0.2: 'blue',
                0.4: 'green',
                0.6: 'yellow',
                0.8: 'orange',
                1.0: 'red'};

        L.heatLayer(heatMapData, {
            maxZoom: 17,
            radius: 50,
            max: 1.0,
            blur: 0,
            gradient: gradientColor}).addTo(fileData.layer);
    });
}