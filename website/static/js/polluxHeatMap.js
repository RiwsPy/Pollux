// une classe à utiliser pour chaque map
// include leafPolluxMethod.js

var intensityColor = {
    0.15: 'violet',
    0.2:  'blue',
    0.4:  'lime',
    0.6:  'yellow',
    0.8:  'orange',
    1.0:  'red'
 };

let params = window.location.href.split('/')
var invertIntensity = params[params.length - 1][0] == '-'

var heatLayerDefaultAttr = {
    maxZoom: 20,
    radius: 30,
    max: Math.min(1, Math.max(0, ...Object.keys(intensityColor))),
    blur: 0,
    gradient: intensityColor
 };


class conflictHeatMap {
    constructor(fileLayer, options) {
        this._options = {
            ...{
                legend: true,
                fullScreenButton: true,
                descButton: true,
                homeButton: true,
            },
            ...options
        }

        for (let lyr of fileLayer.layers) {
            lyr.layer = new L.FeatureGroup();
        }

        this.fileLayer = fileLayer;

        let controlLayers = this.createLayers();
        this.createMap(controlLayers);
        this.loadJsonAndLayer(fileLayer);

        // basic leaflet traduction
        document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
        document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';
    }

    createLayers() {
        let baseClickableZone = createRectangle(defaultZoneBound(), 'yellow'); // rectangle représentant la zone de test
        this._baseLayer = new L.FeatureGroup([baseClickableZone]); // calque contenant le rectangle

        var controlLayers = {
            "Zone Test": this._baseLayer,
        };
        for (let fileData of this.fileLayer.layers) {
            controlLayers[fileData.layerName] = fileData.layer
        };
        return controlLayers
    }

    createMap(controlLayers) {
        this.map = L.map('city_map', {
                layers: [this._baseLayer, this.fileLayer.layers[0].layer],
                minZoom: 15,
            }).setView(defaultZoneBound().getCenter(), 16);

        L.control.layers(null, controlLayers).addTo(this.map);
        addAttribution(this.map, this.fileLayer.legendName)

        if (this._options.fullScreenButton) {
            this.addFullScreenButton()
        }
        if (this._options.legend) {
            this.addLegend(this.fileLayer)
        }
        if (this._options.descButton) {
            addDescButton(this.map)
        }
        if (this._options.homeButton) {
            addHomeButton(this.map)
        }
    }

    addFullScreenButton() {
        this.map.addControl(new L.Control.Fullscreen({
            title: {
                'false': 'Vue plein écran',
                'true':  'Quitter le plein écran'
            }
        }));
    }

    addLegend(fileLayer, position) {
        if (this._mapLegend) {
            this.updateLegend(fileLayer)
        } else {
            var legend = L.control({ position: position || "bottomright" });
            this._mapLegend = legend;
            let ret = this.updateLegend(fileLayer)
            legend.onAdd = function(map) {
                return ret
            };
            legend.addTo(this.map);
        }
    }

    updateLegend(fileLayer) {
        var div = L.DomUtil.create("div", "legend");
        div.innerHTML += "<h4>" + fileLayer.legendName + "</h4>"

        let i = 0;
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
                    this.loadNodeJson(data, layerdata, fileData)
                };
            }
        });
    }

    loadNodeJson(data, layerdata, fileData) {
        let layerName1 = fileData.layers[0].layerName
        L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                if (feature.properties.values[layerName1] > 0) {
                    let marker = L.marker(latlng, {icon: getIcon(layerdata)});
                    addPopUp(feature, marker, layerdata.entityType);
                    return marker;
                }
            }
        }).addTo(layerdata.layer);
    }

    createHeatLayer(data, layerdata) {
        let heatMapData = [];
        data.features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                let intensity = Math.min(1, d.properties.values[layerdata.layerName])
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
}
