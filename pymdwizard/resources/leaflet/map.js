var southWest = L.latLng(-90, -180);
var northEast = L.latLng(90, 180);
var bounds = L.latLngBounds(southWest, northEast);





var map = L.map(
    'map',
    {center: [45.5236,-115.675],
        zoom: 10,
        maxBounds: bounds,
        layers: [],
        worldCopyJump: false,
        crs: L.CRS.EPSG3857
    });



var tile_layer = L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        maxZoom: 18,
        minZoom: 1,
        continuousWorld: false,
        noWrap: false,
        attribution: 'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.',
        detectRetina: false
    }
).addTo(map);

var e_marker = new L.marker([45.5,-115.6],{
    draggable: true
}).addTo(map);

var w_marker = new L.marker([45.5,-115.7],{
    draggable: true
}).addTo(map);

var n_marker = new L.marker([45.6,-115.65],{
    draggable: true
}).addTo(map);

var s_marker = new L.marker([45.4,-115.65],{
    draggable: true
}).addTo(map);

// marker.on("drag", function(e) {
//     var marker = e.target;
//     var position = marker.getLatLng();
//     map.panTo(new L.LatLng(position.lat, position.lng));
// });


// var marker2 = L.marker(map.getCenter()).addTo(map);
// marker2.bindPopup("Hello World  2!").openPopup();
//
if(typeof MainWindow != 'undefined') {
    var onMapMove = function() { MainWindow.on_e_move(e_marker.getLatLng().lat, e_marker.getLatLng().lng) };
    e_marker.on('move', onMapMove);
    onMapMove();
}

if(typeof MainWindow != 'undefined') {
    var onMapMove = function() { MainWindow.onMapMove(w_marker.getLatLng().lat, w_marker.getLatLng().lng) };
    w_marker.on('move', onMapMove);
    onMapMove();
}

if(typeof MainWindow != 'undefined') {
    var onMapMove = function() { MainWindow.onMapMove(e_marker.getLatLng().lat, e_marker.getLatLng().lng) };
    e_marker.on('move', onMapMove);
    onMapMove();
}

if(typeof MainWindow != 'undefined') {
    var onMapMove = function() { MainWindow.onMapMove(e_marker.getLatLng().lat, e_marker.getLatLng().lng) };
    e_marker.on('move', onMapMove);
    onMapMove();
}