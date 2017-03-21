var east = east_var;
var west = west_var;
var north = north_var;
var south = south_var;

var h_center = (east + west) / 2;
var v_center = (north + south) / 2;

var southWest = new L.latLng(south, west);
var northEast = new L.latLng(north, east);
var bounds = new L.latLngBounds(southWest, northEast);





var map = new L.map(
    'map'
    // {center: [v_center, h_center],
    //     zoom: 10,
    //     maxBounds: bounds,
    //     layers: [],
    //     worldCopyJump: true,
    //     crs: L.CRS.EPSG3857
    // }
    );



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

var e_marker = new L.marker([v_center, east],{
    draggable: true
}).addTo(map);

var w_marker = new L.marker([v_center, west],{
    draggable: true
}).addTo(map);

var n_marker = new L.marker([north, h_center],{
    draggable: true
}).addTo(map);


var s_marker = new L.marker([south, h_center],{
    draggable: true
}).addTo(map);



var rect = new L.rectangle(bounds, {color: 'blue', weight: 1}).addTo(map);
map.fitBounds(bounds);

south = south-1;
s_marker.update();

if(typeof Spdom != 'undefined') {
    var onEMove = function () {
        Spdom.on_e_move(e_marker.getLatLng().lat, e_marker.getLatLng().lng)
    };
    e_marker.on('move', onEMove);

    var onWMove = function () {
        Spdom.on_w_move(w_marker.getLatLng().lat, w_marker.getLatLng().lng)
    };
    w_marker.on('move', onWMove);

    var onNMove = function () {
        Spdom.on_n_move(n_marker.getLatLng().lat, n_marker.getLatLng().lng)
    };
    n_marker.on('move', onNMove);

    var onSMove = function () {
        Spdom.on_s_move(s_marker.getLatLng().lat, s_marker.getLatLng().lng)
    };
    s_marker.on('move', onSMove);
}

