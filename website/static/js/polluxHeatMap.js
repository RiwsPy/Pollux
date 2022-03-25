// une classe à utiliser pour chaque map

var defaultZonePos = [[45.187501, 5.704696], [45.198848, 5.725703]];

var legendData = {
    white:  "0 contradiction",
    violet: "0 < I < 0.2",
    blue:   "0.2 < I < 0.4",
    green:  "0.4 <= I < 0.6",
    yellow: "0.6 <= I < 0.8",
    orange: "0.8 <= I < 1",
    red:    "I >= 1",
};

var intensityColor = {
    0.1: 'violet', // non impactant si fixé à 0
    0.2: 'blue',
    0.4: 'green',
    0.6: 'yellow',
    0.8: 'orange',
    1.0: 'red'
 };

 var heatLayerDefaultAttr = {
    maxZoom: 15,
    radius: 50,
    max: Math.min(1, Math.max(0, ...Object.keys(intensityColor))),
    blur: 0,
    gradient: intensityColor
 };


class conflictHeatMap {
    constructor(fileLayer) {
        let lyr;
        for (lyr of fileLayer) {
            lyr.layer = new L.FeatureGroup();
        }

        this.fileLayer = fileLayer;

        this.createMapAndLayers()

        this.loadJsons()
    }

    createMapAndLayers() {
        let clickZoneBound = L.latLngBounds(defaultZonePos); // zone de test
        let baseClickableZone = this.createRectangle(clickZoneBound); // rectangle représentant la zone de test
        let baseLayer = new L.FeatureGroup([baseClickableZone]); // calque contenant le rectangle

        var controlLayers = {
            "Base": baseLayer,
        };
        for (let fileData of this.fileLayer) {
            controlLayers[fileData.layername] = fileData.layer}

        this.map = L.map('city_map', {
                layers: [baseLayer, this.fileLayer[0].layer],
                minZoom: 15,
            }).setView(clickZoneBound.getCenter(), 16);

        L.control.layers(null, controlLayers).addTo(this.map);
        this.addAttribution()
        this.addControl()
        this.addLegend()
        this.addHomeButton()
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
        // Active legend
        var legend = L.control({ position: "bottomright" });

        legend.onAdd = function(map) {
            var div = L.DomUtil.create("div", "legend");
            div.innerHTML += "<h4>Intensité (I)</h4>"
            for (let [color, txt] of Object.entries(legendData)) {
                div.innerHTML += '<i style="background: ' + color + '"></i><span>' + txt + '</span><br>'
            }
            return div;
        };
        legend.addTo(this.map);
    }

    loadJsons() {
        let fileData;
        for (fileData of this.fileLayer) {
            this.loadJson(fileData)
        }
    }

    loadJson(fileData) {
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
                        ...d.geometry.coordinates,
                        +d.properties.intensity]);
                }
            });

            L.heatLayer(heatMapData, heatLayerDefaultAttr).addTo(fileData.layer);
        });
    }

    createRectangle(bound, color, fillColor, fillOpacity) {
        return L.rectangle(bound, {
            color: color || 'yellow',
            fillColor: fillColor || '#3c0',
            fillOpacity: fillOpacity || 0.1,
        })
    }

    addHomeButton() {
        let homeButton = L.control({ position: "topleft" });
        homeButton.onAdd = function(map) {
            let div = L.DomUtil.create("div");
            div.innerHTML += '<a id="goHomeButton" href="/"><i class="fas fa-door-open"></i></a>'
            this._map = map;
            return div;
        };
        homeButton.addTo(this.map);
    }
}

