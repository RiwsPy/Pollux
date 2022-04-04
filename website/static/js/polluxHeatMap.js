// une classe à utiliser pour chaque map
// include leafPolluxMethod.js

var defaultZonePos = [[45.187501, 5.704696], [45.198848, 5.725703]];

var legendData = {
    red:    "_ >= 1",
    orange: "0.8 <= _ < 1",
    yellow: "0.6 <= _ < 0.8",
    green:  "0.4 <= _ < 0.6",
    blue:   "0.2 <= _ < 0.4",
    violet: "0 < _ < 0.2",
    white:  "0: rien à signaler",
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
    radius: 30,
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

        this.createMapAndLayers(fileLayer)

        this.loadJsonAndLayer(fileLayer);
    }

    createMapAndLayers(fileLayer) {
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
        this.addAttribution(fileLayer)
        this.addControl()
        this.addLegend(fileLayer)
        this.addButton('desc')
        this.addButton('home')
    }

    addAttribution(fileLayer) {
        L.tileLayer('https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
            maxZoom: 20,
            attribution: '<a href="https://green-pollux.herokuapp.com">Pollux ' + fileLayer.legendName + '</a>, &copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
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

    addLegend(fileLayer) {
        if (this._mapLegend) {
            this.updateLegend(fileLayer)
        } else {
            var legend = L.control({ position: "bottomright" });
            this._mapLegend = legend;
            let ret = this.updateLegend(fileLayer)
            legend.onAdd = function(map) {
                return ret
            };
            legend.addTo(this.map);
        }
    }

    updateLegend(fileLayer) {
        let legendUnit = fileLayer.legendUnit || fileLayer.legendName[0];

        var div = L.DomUtil.create("div", "legend");
        //div.innerHTML += "<h4>" + fileLayer.legendName + ' (' + legendUnit + ')' + "</h4>"
        div.innerHTML += "<h4>" + fileLayer.legendName + "</h4>"
        let i = 0;
        /*
        for (let [color, txt] of Object.entries(legendData)) {
            div.innerHTML += '<i id="legendButton_' + i + '" style="background: ' + color + '"></i>'
            txt = txt.replace("_", legendUnit);
            div.innerHTML += '<span>' + txt + '</span><br>'
            i += 1;
        }
        */
        for (let [value, color] of Object.entries(intensityColor).sort().reverse()) {
            div.innerHTML += '<i id="legendButton_' + i + '" style="background: ' + color + '"></i>'
            div.innerHTML += '<span>' + ' >= ' + '<span id="legendValue_' + i + '">' + value + '</span>' + '</span><br>'
            i += 1;
        }
        return div;
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
                if (layerdata.layerType == 'heatmap') {
                    this.createHeatLayer(data, layerdata)
                } else if (layerdata.layerType == 'node') {
                    this.loadNodeJson(data, layerdata)
                };
            }
        });
    }

    loadNodeJson(data, fileData) {
        L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                if (feature.properties.intensity.day > 0) {
                    let marker = L.marker(latlng, {icon: getIcon(fileData)});
                    addPopUp(feature, marker, fileData.entityType);
                    return marker;
                }
            }
        }).addTo(fileData.layer);
    }

    createHeatLayer(data, layerdata) {
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
