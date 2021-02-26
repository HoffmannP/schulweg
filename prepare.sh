#!/bin/bash

# https://github.com/fossgis-routing-server/osrm-backend
# http://project-osrm.org/docs/v5.23.0/api

DIRECTORY="OSRM"
PROFILE="foot"

echo <<EOT
Usage:
$0 [--preprocessing (CH|MLD)] file|state

    Contraction Hierarchies (CH)
    Multi-Level Dijkstra (MLD) [default]

    file
    osm.pbf-File|state of germany
EOT

preprocessing="mld"
if [[ "$1" = "--preprocessing" ]] || [[ "$1" = "-pp" ]]; then
    preprocessing="$2"
    file="$3"
else
    file="$1"
fi

if [[ ! -d "$DIRECTORY" ]]; then
    mkdir "$DIRECTORY"
fi
cd "$DIRECTORY"

if [[ ! ( -f "$file" ) ]]; then
    osrm="$file-latest.osrm"
    file="$file-latest.osm.pbf"
    wget http://download.geofabrik.de/europe/germany/$file
fi

docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/${PROFILE}.lua /data/$file

if [[ "$preprocessing" = "ch" ]]; then
    docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-contract /data/$osrm
else
    docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/$osrm
    docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/$osrm
fi

echo "Start with docker run -d --name osrm  -p 5000:5000 -v "${PWD}/OSRM:/data" osrm/osrm-backend osrm-routed --algorithm $preprocessing /data/$osrm"
