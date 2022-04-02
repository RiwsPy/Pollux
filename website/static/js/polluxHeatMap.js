// une classe à utiliser pour chaque map

var defaultZonePos = [[45.187501, 5.704696], [45.198848, 5.725703]];

var legendTitle = 'Impact (I)';
var legendData = {
    white:  "0: rien à signaler",
    violet: "0 < I < 0.2",
    blue:   "0.2 <= I < 0.4",
    green:  "0.4 <= I < 0.6",
    yellow: "0.6 <= I < 0.8",
    orange: "0.8 <= I < 1",
    red:    "I >= 1",
};

var intensityColor = {
    0: 'white',
    0.1: 'violet', // non impactant si fixé à 0
    0.2: 'blue',
    0.4: 'green',
    0.6: 'yellow',
    0.8: 'orange',
    1.0: 'red'
 };

let params = window.location.href.split('/')
var invertIntensity = parseInt(params[params.length - 1]) < 0

var heatLayerDefaultAttr = {
    maxZoom: 15,
    radius: 50,
    max: Math.min(1, Math.max(0, ...Object.keys(intensityColor))),
    blur: 0,
    gradient: intensityColor
 };


class conflictHeatMap {
    constructor(fileLayer) {
        for (let lyr of fileLayer.layers) {
            lyr.layer = new L.FeatureGroup();
        }

        this.fileLayer = fileLayer;

        this.createMapAndLayers()

        this.loadJsonAndLayer(fileLayer);
    }

    createMapAndLayers() {
        let clickZoneBound = L.latLngBounds(defaultZonePos); // zone de test
        let baseClickableZone = this.createRectangle(clickZoneBound); // rectangle représentant la zone de test
        let baseLayer = new L.FeatureGroup([baseClickableZone]); // calque contenant le rectangle

        var controlLayers = {
            "Zone Test": baseLayer,
        };
        for (let fileData of this.fileLayer.layers) {
            controlLayers[fileData.layerName] = fileData.layer
        };

        this.map = L.map('city_map', {
                layers: [baseLayer, this.fileLayer.layers[0].layer],
                minZoom: 15,
            }).setView(clickZoneBound.getCenter(), 16);

        L.control.layers(null, controlLayers).addTo(this.map);
        this.addAttribution()
        this.addControl()
        this.addLegend()
        this.addButton('desc')
        this.addButton('home')
    }

    addAttribution() {
        L.tileLayer('https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
            maxZoom: 20,
            attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
            }).addTo(this.map);
    }

    addControl() {
        // Active control buttons
        this.map.addControl(new L.Control.Fullscreen({
            title: {
                'false': 'Vue plein écran',
                'true':  'Quitter le plein écran'
            }
        }));
    }

    addLegend() {
        var legend = L.control({ position: "bottomright" });

        legend.onAdd = function(map) {
            var div = L.DomUtil.create("div", "legend");
            div.innerHTML += "<h4>" + legendTitle + "</h4>"
            for (let [color, txt] of Object.entries(legendData)) {
                div.innerHTML += '<i style="background: ' + color + '"></i><span>' + txt + '</span><br>'
            }
            return div;
        };
        legend.addTo(this.map);
    }

    loadJsonAndLayer(fileData) {
        let request = new Request('/api/' + fileData.filename, {
            method: 'GET',
            headers: new Headers(),
        })

        fetch(request)
        .then((resp) => resp.json())
        .then((data) => {
            for (let layerdata of this.fileLayer.layers) {
                let heatMapData = [];
                data.features.forEach(function(d) {
                    if (d.geometry.type == 'Point') {
                        let intensity = Math.min(1, d.properties.intensity[layerdata.intensityKey])
                        intensity = invertIntensity ? 1-intensity : intensity
                        heatMapData.push([
                            // TODO: change this bullshit
                            +Math.max(...d.geometry.coordinates),
                            +Math.min(...d.geometry.coordinates),
                            //
                            +intensity]);
                    }
                });
                L.heatLayer(heatMapData, heatLayerDefaultAttr).addTo(layerdata.layer);
            }
        });
    }

    createRectangle(bound, color, fillColor, fillOpacity) {
        return L.rectangle(bound, {
            color: color || 'yellow',
            fillColor: fillColor || '#3c0',
            fillOpacity: fillOpacity || 0.1,
        })
    }

    addButton(functionButton) {
        let homeButton = L.control({ position: "topleft" });
        homeButton.onAdd = function(map) {
            let div = L.DomUtil.create("div");
            if (functionButton == 'desc') {
                let url = new URL(window.location.href)
                let url_split = url.pathname.split('/')
                let map_id = url_split[2]
                div.innerHTML += '<a id="mapButton" href="/map_desc/' + map_id + '" title="Ouvrir la description" target="_blank"><i style="width: 17px;" class="fa fa-book fa-lg"></i></a>'
            } else if (functionButton == 'home') {
                div.innerHTML += '<a id="mapButton" href="/" title="Retour à l\'accueil"><i class="fas fa-door-open"></i></a>'
            }
            this._map = map;
            return div;
        };
        homeButton.addTo(this.map);
    }
}
