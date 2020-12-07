#!/bin/bash

# Update 
sudo apt-get update -y;
sudo apt-get install -y python3 python3-pip python3-dev build-essential golang wget unzip mariadb-server libmariadb-dev-compat;

# Install python modules
pip3 install -r requirements.txt;

# Setting go paths
echo "export GOPATH=$HOME/go;
export PATH=$PATH:$GOPATH/bin;" >> ~/.profile;
source ~/.profile;

# Install Newer Version of golang
go get golang.org/dl/go1.13.4;
go1.13.4 download;

# Installing tools
go1.13.4 get -u -v github.com/OJ/gobuster;
go get github.com/cgboal/sonarsearch/crobat;
go1.13.4 get -u -v github.com/melbadry9/enumsho;
go1.13.4 get -u -v github.com/melbadry9/subover;
go1.13.4 get -u -v github.com/tomnomnom/httprobe;
go1.13.4 get -u -v github.com/tomnomnom/assetfinder;
go1.13.4 get -u -v github.com/projectdiscovery/nuclei/cmd/nuclei;
go1.13.4 get -u -v github.com/projectdiscovery/subfinder/cmd/subfinder;
go1.13.4 get -u -v github.com/projectdiscovery/chaos-client/cmd/chaos;

# Amass
wget https://github.com/OWASP/Amass/releases/download/v3.6.0/amass_v3.6.0_linux_amd64.zip;
unzip -j amass_v3.6.0_linux_amd64.zip amass_v3.6.0_linux_amd64/amass -d ${GOPATH}/bin/;
rm amass_v3.6.0_linux_amd64.zip;

# Findomain
wget https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux;
chmod +x findomain-linux;
mv findomain-linux ${GOPATH}/bin/findomain;