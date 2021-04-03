import * as Leaflet from './leaflet-src.esm'
import './Leaflet.fullscreen'
import createLayers from './layers'

import './leaflet.css'
import './leaflet.fullscreen.css'
import './style.css'

document.addEventListener('DOMContentLoaded', function () {
  woopra()

  const map = Leaflet
    .map('map', { zoomSnap: 0.2, fullscreenControl: true })
    .fitBounds([
      [50.990, 11.498],
      [50.856, 11.673]
    ])

  createLayers(Leaflet, map)

  Leaflet.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: [
      'Map data © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>'
    ].join(', '),
    maxZoom: 20,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYmVyZW5nYXIiLCJhIjoiY2tsdHZodWRrMGdyZDJubjhlNGZpNGprYyJ9.cSvy6HHHiFdzQGHUl5TVsg'
  }).addTo(map)
})
