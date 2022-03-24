// une classe à utiliser pour chaque map


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
        let clickZoneBound = L.latLngBounds([[45.187501, 5.704696], [45.198848, 5.725703]]);
        let baseClickableZone = this.createRectangle(clickZoneBound);
        let baseLayer = new L.FeatureGroup([baseClickableZone]);
        let fileData;

        var controlLayers = {
            "Base": baseLayer,
        };
        for (fileData of this.fileLayer) {
            controlLayers[fileData.layername] = fileData.layer}

        this.map = L.map('city_map', {
                layers: [baseLayer, this.fileLayer[0].layer],
                minZoom: 15,
            }).setView(clickZoneBound.getCenter(), 16);

        L.control.layers(null, controlLayers).addTo(this.map);
        this.addAttribution()
        this.addControl()
        this.addLegend()
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
                'true': 'Quitter le plein écran'
            }
        }));
    }

    addLegend() {
        // Active legend
        var legend = L.control({ position: "bottomright" });

        legend.onAdd = function(map) {
            var div = L.DomUtil.create("div", "legend");
            div.innerHTML += "<h4>Intensité (I)</h4>";
            div.innerHTML += '<i style="background: white"></i><span>0 contradiction</span><br>';
            div.innerHTML += '<i style="background: blue"></i><span>0 \< I < 0.3</span><br>';
            div.innerHTML += '<i style="background: green"></i><span>0.3 \<= I < 0.5</span><br>';
            div.innerHTML += '<i style="background: yellow"></i><span>0.5 \<= I < 0.7</span><br>';
            div.innerHTML += '<i style="background: orange"></i><span>0.7 \<= I < 0.9</span><br>';
            div.innerHTML += '<i style="background: red"></i><span>I >= 0.9</span><br>';
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
                        +d.geometry.coordinates[0],
                        +d.geometry.coordinates[1],
                        +d.properties.intensity]);
                }
            });

            let gradientColor = {
                    0.15: 'violet',
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

    createRectangle(bound, color, fillColor, fillOpacity) {
        return L.rectangle(bound, {
            color: color || 'yellow',
            fillColor: fillColor || '#3c0',
            fillOpacity: fillOpacity || 0.1,
        })
    }
}

