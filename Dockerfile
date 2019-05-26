FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential tor
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN echo "ControlPort 9051" >> /etc/tor/torrc
RUN echo "HashedControlPassword 16:59E63A18DADECFBE602D5F8453B80205044A6C89A65E531C75D27558D8" >> /etc/tor/torrc
RUN service tor start
RUN chmod 777 subover/subover
RUN chmod 777 Gobuster/gobuster