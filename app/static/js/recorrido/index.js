// DECLARACIONES
const initialLat = -34.9187
const initialLang = -57.956
var mymap = L.map('map_recorrido').setView([-34.9187, -57.956], 13)
var popup = L.popup()
var marker

let editableLayers = new L.FeatureGroup()

let controls = new L.Control.Draw({
  draw: {
    marker: true,
    circlemarker: false,
    polygon: false,
    rectangle: false,
    circle: false,
    polyline: false,
  },
  edit: {
    featureGroup: editableLayers, //REQUIRED!!
    remove: true,
  },
})

mymap.addControl(controls)

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 20,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
}).addTo(mymap)

let cant = 0
let arreglo_coordenadas = []
function hizoClic(e) {
  console.log(e)
  let arreglo_aux = []
  arreglo_aux.push(e.latlng.lat, e.latlng.lng)
  arreglo_coordenadas.push(arreglo_aux)

  marker = L.marker({ lon: e.latlng.lng, lat: e.latlng.lat }).addTo(mymap)
  L.popup()
    .setLatLng([e.latlng.lat, e.latlng.lng])
    .setContent(`Punto número ${cant + 1} `)
    .openOn(mymap)

  cant = cant + 1

  if (cant > 1) {
    let poly = []
    arreglo_coordenadas.forEach((element) => {
      poly.push(element)
    })
    let arreglo
    arreglo = JSON.stringify(arreglo_coordenadas)
    console.log(arreglo)

    document
      .getElementById('arreglo_coordenadas')
      .setAttribute('value', arreglo)
    console.log(poly)

    let polyline = L.polyline(poly, { color: 'red' }).addTo(mymap)
    // aca le paso el polyline
    mymap.fitBounds(polyline.getBounds())
  }
}

mymap.on('click', hizoClic)
