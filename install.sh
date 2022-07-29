#!/bin/bash

# Update 
sudo apt-get update -y;
sudo apt-get install -y python3 python3-pip python3-dev build-essential golang wget unzip mariadb-server libmariadb-dev-compat libmariadbd-dev;

# Install python modules
pip3 install -r requirements.txt;

# Setting go paths
echo "export GOPATH=$HOME/go;
export PATH=$PATH:$GOPATH/bin;" >> ~/.profile;
source ~/.profile;

# Install Newer Version of golang
go get golang.org/dl/go1.17;
go1.17 download;

go get -v github.com/melbadry9/enumsho
go1.17 get -v github.com/cgboal/sonarsearch/cmd/crobat
go1.17 install -v github.com/tomnomnom/httprobe@latest
go1.17 install -v github.com/tomnomnom/assetfinder@latest
go1.17 install -v github.com/melbadry9/subover@latest
go1.17 install -v github.com/OJ/gobuster/v3@latest
go1.17 install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go1.17 install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go1.17 install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go1.17 install -v github.com/projectdiscovery/chaos-client/cmd/chaos@latest

wget --quiet https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux
chmod +x findomain-linux
mv findomain-linux ${GOPATH}/bin/findomain

wget --quiet https://github.com/OWASP/Amass/releases/download/v3.19.3/amass_linux_amd64.zip
unzip -j amass_linux_amd64.zip amass_linux_amd64/amass -d ${GOPATH}/bin/
rm amass_linux_amd64.zip