#!/bin/bash

docker rm -f osrm
docker run -d --name osrm  -p 5000:5000 -v "${PWD}/OSRM:/data"     osrm/osrm-backend osrm-routed --algorithm mld /data/thueringen-latest.osrm
