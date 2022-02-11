import { ZoneMap } from '../../js/zonas/ZoneMap.js'

window.onload = () => {
  let coords = document.getElementById('coords').innerHTML
  let coords2 = JSON.parse(coords)
  let color = document.getElementById('color').innerHTML
  let fig = {
    marker: false,
    circlemarker: false,
    polygon: false,
    rectangle: false,
    circle: false,
    polyline: false,
  }
  const map = new ZoneMap({
    color: color,
    coords: coords2,
    selector: 'mapid',
    fig: fig,
  })
}
