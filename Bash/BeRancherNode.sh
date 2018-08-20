#!/bin/bash
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install docker.io -y
systemctl start docker
systemctl enable docker
pip install netifaces

myAddr=$(python getMyAddr.py)
sudo docker run -e CATTLE_AGENT_IP=$(myAddr)  --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.2.11 http://45.76.106.129:8080/v1/scripts/16E0A6897EFFC6137F70:1514678400000:8mMqdlJChjjwdTiinJy3OjovFG8
