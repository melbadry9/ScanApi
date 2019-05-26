#/bin/bash/
apt-get update -y;
apt-get install -y python3 python3-pip python3-dev build-essential tor;
pip3 install -r requirements.txt;
echo "ControlPort 9051" >> /etc/tor/torrc;
echo "HashedControlPassword 16:59E63A18DADECFBE602D5F8453B80205044A6C89A65E531C75D27558D8" >> /etc/tor/torrc;
service tor start;
chmod 777 subover/subover;
chmod 777 Gobuster/gobuster;
