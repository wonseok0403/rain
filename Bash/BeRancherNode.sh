#!/bin/bash
#sudo apt-get install \
#    udo docker run -d --restart=unless-stopped -ppt-transport-https \
#    ca-certificates \
#    curl \
#    software-properties-common -y
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#sudo add-apt-repository \
#   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) \
#   stable"
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install docker.io -y
sudo apt-get install python-pip
pip install netifaces
myAddr=$(python getMyAddr.py)
sudo docker run -e CATTLE_AGENT_IP=$(myAddr)  --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/rancher:/var/lib/rancher rancher/agent:v1.2.11 http://45.76.106.129:8080/v1/scripts/972F2925FA3C0F83D400:1514678400000:x5QqxLU5cGfNxdu3n7kEU1GwJ8
