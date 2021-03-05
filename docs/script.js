/* global L */

const colormap = {
  'Friedrich-Schiller': '#db2897',
  'Heinrich-Heine': '#0c98cf',
  Nordschule: '#58c9c0',
  Saaletalschule: '#3e76d5',
  'Schule am Rautal': '#4446dc',
  Südschule: '#ebcb48',
  Talschule: '#b27acc',
  Westschule: '#26ea51',

  'An der Trießnitz': '#25ea95',
  Galileo: '#5316cd',
  'Jenaplan-Schule': '#d63ad1',
  Kaleidoskop: '#c8768c',
  Kulturanum: '#d95346',
  Lobdeburgschule: '#97e289',
  Montessorischule: '#ce8549',
  Wenigenjena: '#b8ca51',
  Werkstattschule: '#81d62b'
}

function colorize (property) {
  return feature => ({
    color: colormap[feature.properties[property]]
  })
}

const map = L.map('map').setView([50.92, 11.59], 12.4)
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 18,
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1,
  accessToken: 'pk.eyJ1IjoiYmVyZW5nYXIiLCJhIjoiY2tsdHZodWRrMGdyZDJubjhlNGZpNGprYyJ9.cSvy6HHHiFdzQGHUl5TVsg'
}).addTo(map)
const control = L.control.layers().addTo(map)
const layers = [
  {
    file: 'alle',
    layer: 'Alle Schultypen',
    property: 'naechste_i'
  },
  {
    file: 'gms',
    layer: 'Nur Gemeinschaftsschulen',
    property: 'naechste_4'
  },
  {
    file: 'grund',
    layer: 'Nur Grundschulen',
    property: 'naechste_g'
  }
]
let first = true
for (const layer of layers) {
  window.fetch(`${layer.file}.geojson`)
    .then(r => r.json())
    .then(function (feature) {
      const l = L.geoJSON(feature, { style: colorize(layer.property) })
      l.bindPopup(l => l.feature.properties[layer.property])
      control.addBaseLayer(l, layer.layer)
      if (first) {
        l.addTo(map)
        first = false
      }
    })
}

(function () {
  var t; var i; var e; var n = window; var o = document; var a = arguments; var s = 'script'; var r = ['config', 'track', 'identify', 'visit', 'push', 'call', 'trackForm', 'trackClick']; var c = function () { var t; var i = this; for (i._e = [], t = 0; r.length > t; t++)(function (t) { i[t] = function () { return i._e.push([t].concat(Array.prototype.slice.call(arguments, 0))), i } })(r[t]) }; for (n._w = n._w || {}, t = 0; a.length > t; t++)n._w[a[t]] = n[a[t]] = n[a[t]] || new c(); i = o.createElement(s), i.async = 1, i.src = '//static.woopra.com/js/w.js', e = o.getElementsByTagName(s)[0], e.parentNode.insertBefore(i, e)
})('woopra')
woopra.config({
  domain: 'ichplatz.de'
})
woopra.track()
