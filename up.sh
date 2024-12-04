#!/bin/bash
docker compose up -d
echo "SMP http://localhost:8882/csp/sys/%25CSP.Portal.Home.zen"
echo "see send.sh to send mqtt data"
docker compose exec iris bash -c "pip install -r /share/requirments.txt -t /iris-mgr/data/mgr/python"
docker compose exec iris bash -c "pip install -r /share/requirments.txt"
