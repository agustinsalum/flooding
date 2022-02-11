// initialize Leaflet
var map = L.map('mapid').setView({lon: -60.569722, lat: -36.157222}, 5);
var marker;
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    minZoom: 5,
}).addTo(map);

function onMapClick(e) {
	document.getElementById('corx').setAttribute('value', e.latlng.lat)
	document.getElementById('cory').setAttribute('value', e.latlng.lng)
	if (marker) marker.remove();
	marker = L.marker({lon:  e.latlng.lng, lat: e.latlng.lat}).bindPopup('Denuncia').addTo(map);
}
map.on('click', onMapClick)

// OTRO EJEMPLO PERO NO FUNCIONA
//var marker1 = L.marker({lon: -57.892863750, lat: -34.876179100}).bindPopup('TITULO DEL MARKER').addTo(map);





/* CODIGO HECHO DE UN VIDEO DE YOUTUBE

var mymap = L.map('mapid').setView([51.505, -0.09], 13);

const initializeMap = (selector) => {
	map = L.map(selector).setView([-34.9187,-57.956],13);
	L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
	map.on('click', mapClickHandler)
}

const mapClickHandler = (e) => {
	addMarker(e.latlng);
}
const addMarker = ({ lat , lng }) => {
	if (marker) marker.remove();
	marker = L.marker([lat,lng]).addTo(map);
}

const submitHandler = (event) => {
	if (!marker) {
		event.preventDefault();
		alert('Debes seleccionar una ubicación en el mapa.')
	}
	else {
		latlng = marker.getLatLng();
		document.getElementById('corx').setAttribute('value', latlng.lat)
		document.getElementById('cory').setAttribute('value', latlng.lng)
	}
}


window.onload = () => {

	initializeMap('mapid');
}
*/