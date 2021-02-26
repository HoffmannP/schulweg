#!/bin/bash

docker rm -f osrm
docker run -d --name osrm  -p 5000:5000 -v "${PWD}/OSRM:/data"     osrm/osrm-backend osrm-routed --algorithm mld /data/thueringen-latest.osrm

docker rm -f mongo
docker run -d --name mongo -p 27017:27017 -v "${PWD}/Mongo:/data/db" mongo:3.6