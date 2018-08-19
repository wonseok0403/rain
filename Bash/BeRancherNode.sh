#!/bin/bash
sudo apt-get install \
    udo docker run -d --restart=unless-stopped -ppt-transport-https \
    ca-certificates \
    curl \
    software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update -y
sudo apt-get install docker-ce -y

RANCHER_URL="https://108.61.162.237"
RANCHER_ACCESS_KEY="token-s22d6"
RANCHER_SECRET_KEY="cqzn8j6ddknsz5tsp2d7d4cx8whcc7sr7q9xkxzmjtbmlgc8v2mz5l"
## some host labels as needed
CATTLE_HOST_LABELS="host=$(hostname)&role=development"


## do some stuff like getting jq
sudo curl -skL https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 -o /usr/local/bin/jq
sudo chmod +x /usr/local/bin/jq

## generate rancher registrationtokens
ID=$(curl -X POST \
-u "${RANCHER_ACCESS_KEY}:${RANCHER_SECRET_KEY}" \
-H 'Accept: application/json' \
-H 'Content-Type: application/json' \
-d "{\"name\":\"$(hostname)\"}" \
"${RANCHER_URL}/v3/registrationtokens" | jq -r .id)

## need to wait
sleep 5

COMMAND=$(curl -X GET \
-u "${RANCHER_ACCESS_KEY}:${RANCHER_SECRET_KEY}" \
-H 'Accept: application/json' \
"${RANCHER_URL}/v3/registrationtokens/$ID" | jq -r .command)

## start ranger-agent ~ running with root privileges no need for sudo. 
COMMAND=(docker run -e CATTLE_HOST_LABELS=$CATTLE_HOST_LABELS ${COMMAND#*run})
exec "${COMMAND[@]}"
