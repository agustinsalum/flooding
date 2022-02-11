<template>
  <div>
    <div class="container" @click="$emit('marcarPunto', this.punto)">
      <div id="mapa_simple" ref="mapa_simple"></div>
    </div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
// Debemos instalar "npm install leaflet"
// Necesario para el mapa
import L from 'leaflet'
delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
})

// Necesario para el mapa
export default {
  name: 'Denuncia',
  props: {
    tipo: String,
    data: Array,
  },
  data() {
    return {
      zonas: [],
      punto: {
        latitud: '',
        longitud: '',
      },
    }
  },
  mounted() {
    // Mi mapa de la parte privada
    var mymap = L.map(this.$refs['mapa_simple']).setView(
      [-34.9187, -57.956],
      10
    )
    var marker

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 20,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1,
    }).addTo(mymap)

    function hizoClic(e) {
      document.getElementById('corx').setAttribute('value', e.latlng.lat)
      document.getElementById('cory').setAttribute('value', e.latlng.lng)

      if (marker) marker.remove()
      marker = L.marker({ lon: e.latlng.lng, lat: e.latlng.lat })
        .bindPopup('Denuncia')
        .addTo(mymap)
    }

    function esRecorrido(data) {
      console.log('es recorrido')
      console.log(JSON.parse(JSON.stringify(data)))
      if (JSON.parse(JSON.stringify(data)).length !== 0) {
        if (JSON.parse(JSON.stringify(data))[0] === undefined) {
          let element = JSON.parse(JSON.parse(JSON.stringify(data)).coordenadas)
          let poly = []
          element.forEach((element2) => {
            let a = []
            a.push(element2[0], element2[1])
            poly.push(a)
          })
          let polyline = L.polyline(poly, { color: 'red' }).addTo(mymap)
          // aca le paso el polyline
          mymap.fitBounds(polyline.getBounds())
        } else {
          JSON.parse(JSON.stringify(data)).forEach((element) => {
            let poly = []
            element.coordenadas.forEach((element2) => {
              let a = []
              a.push(element2.lat, element2.long)
              poly.push(a)
            })
            let polyline = L.polyline(poly, { color: 'red' }).addTo(mymap)
            // aca le paso el polyline
            mymap.fitBounds(polyline.getBounds())
          })
        }
      }
    }

    function esPunto(data) {
      console.log('es punto')
      JSON.parse(JSON.stringify(data)).forEach((element, index) => {
        console.log(index)
        marker = L.marker({ lon: element.long, lat: element.lat })
          .bindPopup('Denuncia')
          .addTo(mymap)
      })
    }
    function esZona(data) {
      console.log('es zona')
      // cuando hay data
      if (data !== undefined) {
        // cuando no es un recorrido especifico (no contiene el atributo color)
        if (data.color !== undefined) {
          let poly = []
          data.coords.forEach((element2) => {
            let a = []
            a.push(element2.lat, element2.long)
            poly.push(a)
          })
          let polygon = L.polygon(poly)
          polygon.setStyle({ fillColor: data.color })
          mymap.addLayer(polygon)
        } else {
          JSON.parse(JSON.stringify(data)).forEach((element) => {
            let poly = []
            element.coords.forEach((element2) => {
              let a = []
              a.push(element2.lat, element2.long)
              poly.push(a)
            })
            let polygon = L.polygon(poly)
            polygon.setStyle({ fillColor: element.color })
            mymap.addLayer(polygon)
          })
        }
      }
    }

    // eventos para los distintos tipos de mapa
    switch (this.tipo) {
      case 'denuncia':
        mymap.on('click', hizoClic)
        mymap.on('click', this.marcarPunto)
        break
      case 'punto':
        esPunto(this.data)
        break
      case 'zona':
        esZona(this.data)
        break
      case 'recorrido':
        esRecorrido(this.data)
        break
      default:
        mymap.on('click', console.log('indefinido'))
        break
    }
  },

  methods: {
    // Funcion de methods para asignar a los datos las coordenadas. Es el estado de los datos que estoy manejando

    marcarPunto(e) {
      this.punto.latitud = e.latlng.lat.toString()
      this.punto.longitud = e.latlng.lng.toString()
    },
  },
}
</script>
