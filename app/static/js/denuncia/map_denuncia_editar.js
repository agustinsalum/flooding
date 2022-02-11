// DECLARACIONES
var mymap = L.map('map_denuncia_editar').setView([-34.9187, -57.956], 10);
var popup = L.popup();
var marker;

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
    maxZoom: 20,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);


var latactual = document.getElementById('corx_edit').value
var lonactual = document.getElementById('cory_edit').value
var popup = L.popup()
    .setLatLng([latactual, lonactual])
    .setContent("Ubicación Actual")
    .openOn(mymap);




function hizoClic(e) {
	document.getElementById('corx_edit').setAttribute('value', e.latlng.lat)
	document.getElementById('cory_edit').setAttribute('value', e.latlng.lng)
	if (marker) marker.remove();
	marker = L.marker({lon:  e.latlng.lng, lat: e.latlng.lat}).bindPopup('Denuncia').addTo(mymap);
}



mymap.on('click', hizoClic)