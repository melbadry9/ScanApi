#!/bin/bash/
apt-get update -y;
apt-get install -y python3 python3-pip python3-dev build-essential golang wget unzip git;
pip3 install -r requirements.txt;
export GOPATH=$HOME/go;
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin;
go get -u github.com/melbadry9/subover;
go get -u github.com/OJ/gobuster;
go get -u github.com/tomnomnom/assetfinder;
go get -u github.com/tomnomnom/httprobe;
wget https://github.com/OWASP/Amass/releases/download/v3.1.10/amass_v3.1.10_linux_amd64.zip;
unzip amass_v3.1.10_linux_amd64.zip;
cp amass_v3.1.10_linux_amd64/amass $GOPATH/bin/;
