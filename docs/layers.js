import alle from './alle.geo.json'
import gms from './gms.geo.json'
import grund from './grund.geo.json'
import schulen from './schulen.geo.json'
import colorize from './colormap.js'

const filter = (schulen, typ) => ({ ...schulen, features: schulen.features.filter(f => f.properties.typ === typ) })

var schoolIconOptions = {
  shadowUrl: 'images/school-shaddow.png',

  iconSize: [20, 19], // size of the icon
  shadowSize: [40, 36], // size of the shadow
  iconAnchor: [10, 12], // point of the icon which will correspond to marker's location
  shadowAnchor: [16, 20], // the same for the shadow
  popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
}

const layers = [
  {
    feature: alle,
    name: 'Grund- und Gemeinschaftschulen',
    overlay: false
  },
  {
    feature: gms,
    name: 'Gemeinschaftsschulen',
    overlay: false
  },
  {
    feature: grund,
    name: 'Grundschulen',
    overlay: false
  },
  {
    feature: filter(schulen, 'Grundschule'),
    typ: 'Grundschulen',
    name: '<span style="color:#7b2939">Grundschulen</span>',
    overlay: true
  },
  {
    feature: filter(schulen, 'Gemeinschaftsschule'),
    typ: 'Gemeinschaftsschulen',
    name: '<span style="color:#3a5680">Gemeinschaftsschulen</span>',
    overlay: true
  }
]

export default function (Leaflet, map) {
  const schoolIcons = {
    Grundschulen: Leaflet.icon({ ...schoolIconOptions, iconUrl: 'images/school-gs.png' }),
    Gemeinschaftsschulen: Leaflet.icon({ ...schoolIconOptions, iconUrl: 'images/school-gms.png' })
  }
  const control = Leaflet.control.layers().addTo(map)

  layers.forEach(function (l, i) {
    const layer = Leaflet
      .geoJSON(l.feature, { style: colorize, pointToLayer: (geoJsonPoint, latlng) => Leaflet.marker(latlng, { icon: schoolIcons[l.typ] }) })
      .bindPopup(l => l.feature.properties.name)
    control[l.overlay ? 'addOverlay' : 'addBaseLayer'](layer, l.name)
    if ((i === 0) || l.overlay) {
      layer.addTo(map)
    }
  })
}
