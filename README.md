Kartenerzeugung
===============

* Plugin: "OSM Place Search" -> Suche "Jena" -> Objekt zu neuem Layer hinzufügen
* Import "abstaende.geojson", "gemeinschaftsschulen.geojson", "grundschulen.geojson"
* Layer "abstaende" Vektor->Geometrie-Werkzeuge->Voronoi-Polygone
* Layer "Voronoi" Vektor->Geoverarbeitungswerkzeuge->Auflösen nach Eigenschaften
    - naechste_insgesamt
    - naechste_grundschulen
    - naechste_gemeinschaftsschulen
* Aufgelöste Layer Vektor->Geoverarbeitungswerkzeuge->Zuschneiden mit Layer "Jena"
