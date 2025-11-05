#!/bin/bash

# Update 
sudo apt-get update -y;
sudo apt-get install -y python3 python3-pip python3-dev build-essential golang wget unzip mariadb-server libmariadb-dev-compat libmariadbd-dev;

# Install python modules
pip3 install -r requirements.txt;

# Install tools
cat ./go-tools.txt | xargs -n3 -I{} sh -c 'echo "Installing {}" && go install "{}"'

wget --quiet https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux
chmod +x findomain-linux
mv findomain-linux ${GOPATH}/bin/findomain

wget --quiet https://github.com/OWASP/Amass/releases/download/v3.19.3/amass_linux_amd64.zip
unzip -j amass_linux_amd64.zip amass_linux_amd64/amass -d ${GOPATH}/bin/
rm amass_linux_amd64.zip
