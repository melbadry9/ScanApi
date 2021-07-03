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
go get golang.org/dl/go1.13;
go get golang.org/dl/go1.16;
go1.13 download;
go1.16 download;

# Installing tools
go get -v github.com/melbadry9/enumsho;
go1.16 get -v github.com/cgboal/sonarsearch/crobat;
go1.16 get -v github.com/tomnomnom/assetfinder;
go1.16 get -v github.com/tomnomnom/httprobe;
go1.16 get -v github.com/melbadry9/subover;
go1.16 install github.com/OJ/gobuster/v3@latest;
GO111MODULE=on go1.16 get -v github.com/projectdiscovery/httpx/cmd/httpx
GO111MODULE=on go1.16 get -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei;
GO111MODULE=on go1.16 get -v github.com/projectdiscovery/chaos-client/cmd/chaos;
GO111MODULE=on go1.16 get -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder;

# Amass
wget --quiet https://github.com/OWASP/Amass/releases/download/v3.13.2/amass_linux_amd64.zip;
unzip -j amass_linux_amd64.zip amass_linux_amd64/amass -d ${GOPATH}/bin/;
rm amass_linux_amd64.zip;

# Findomain
wget --quiet https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux;
chmod +x findomain-linux;
mv findomain-linux ${GOPATH}/bin/findomain;