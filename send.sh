#!/bin/bash

docker compose exec iris mosquitto_pub -h mqttbroker -p 1883 -t /XGH/PT -f /share/compare.avro
docker compose exec iris mosquitto_pub -h mqttbroker -p 1883 -t /XGH/PYAVRO -f /share/compare.avro
docker compose exec iris mosquitto_pub -h mqttbroker -p 1883 -t /XGH/PYJSON -f /share/compare.json
