const colormap = {
  'Friedrich-Schiller': '#d63ad1',
  'Heinrich-Heine': '#0c98cf',
  Nordschule: '#58c9c0',
  Saaletalschule: '#3e76d5',
  'Schule am Rautal': '#4446dc',
  Südschule: '#ebcb48',
  Talschule: '#b27acc',
  Westschule: '#db2897',

  'An der Trießnitz': '#25ea95',
  Galileo: '#5316cd',
  'Jenaplan-Schule': '#26ea51',
  Kaleidoskop: '#c8768c',
  Kulturanum: '#d95346',
  Lobdeburgschule: '#97e289',
  Montessorischule: '#ce8549',
  Wenigenjena: '#b8ca51',
  Werkstattschule: '#81d62b'
}

export default feature => ({ color: colormap[feature.properties.name] })
