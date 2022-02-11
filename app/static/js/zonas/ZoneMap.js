const initialLat = -34.9187
const initialLang = -57.956
const mapLayerUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

export class ZoneMap {
  #drawnItems
  #figuras

  constructor({ selector, coords, color, fig, type }) {
    this.#figuras = fig
    this.#drawnItems = new L.FeatureGroup()
    console.log(coords.length)

    this.#initializeMap(selector)
    this.map.on(L.Draw.Event.CREATED, (e) => {
      this.#eventHandler(
        e,
        this.map,
        this.#drawnItems,
        this.editControls,
        this.createControls
      )
    })
    this.map.on('draw:deleted', () => {
      this.#deleteHandler(this.map, this.editControls, this.createControls)
    })

    // dentro del constructor, armo el polygon y lo paso a la capa

    let poly = []
    coords.forEach((element) => {
      poly.push(element)
    })

    let polygon = L.polygon(poly)
    // aca le paso el polygon
    polygon.setStyle({ fillColor: color })

    this.map.addLayer(polygon)
  }
  #initializeMap(selector) {
    this.map = L.map(selector).setView([initialLat, initialLang], 13)
    L.tileLayer(mapLayerUrl).addTo(this.map)

    this.map.addLayer(this.#drawnItems)
    this.map.addControl(this.createControls)
  }

  #eventHandler(e, map, drawnItems, editControls, createControls) {
    const existingZones = Object.values(drawnItems._layers)

    if (existingZones.length == 0) {
      const type = e.layerType
      const layer = e.layer

      if (type === 'marker') {
      }

      layer.editing.enable()
      drawnItems.addLayer(layer)
      editControls.addTo(map)
      createControls.remove()
    }
  }
  #deleteHandler(map, editControls, createControls) {
    createControls.addTo(map)
    editControls.remove()
  }

  hasValidZone() {
    return this.drawnLayers.length === 1
  }

  get drawnLayers() {
    return Object.values(this.#drawnItems._layers)
  }

  get editControls() {
    return (this.editControlsToolbar ||= new L.Control.Draw({
      draw: false,
      edit: {
        featureGroup: this.#drawnItems,
      },
    }))
  }

  get createControls() {
    return (this.createControlsToolbar ||= new L.Control.Draw({
      // draw: {
      //   circle: false,
      //   marker: false,
      //   polyline: false,
      // },
      draw: this.#figuras,
    }))
  }
}
