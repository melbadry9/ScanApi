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
go get -u -v github.com/projectdiscovery/subfinder/cmd/subfinder;
wget https://github.com/OWASP/Amass/releases/download/v3.1.10/amass_v3.1.10_linux_amd64.zip;
wget https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux;
chmod +x findomain-linux;
unzip amass_v3.1.10_linux_amd64.zip;
cp findomain-linux $GOPATH/bin/findomain;
cp amass_v3.1.10_linux_amd64/amass $GOPATH/bin/;
