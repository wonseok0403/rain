sudo apt-get remove docker docker-engine docker.io -y
sudo docker run -d --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher

# https://www.npmjs.com/package/rancher-api
