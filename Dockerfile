FROM debian:buster-slim

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential golang wget unzip mariadb-server libmariadb-dev-compat libmariadbd-dev git apache2 libapache2-mod-wsgi-py3

EXPOSE 80
COPY . /var/www/scanapi
WORKDIR /var/www/scanapi
RUN mkdir logs
RUN chmod 777 -R logs

RUN pip3 install -r requirements.txt
RUN python3 manage.py collectstatic
RUN rm ./logs/*

COPY ./scanapi_apache.conf /etc/apache2/sites-available/scanapi.conf
RUN a2ensite scanapi
RUN a2dissite 000-default
RUN service apache2 restart

ENV GOPATH=$HOME/go
ENV PATH=$PATH:${GOPATH}/bin

RUN go get golang.org/dl/go1.17
RUN go1.17 download

RUN go get -v github.com/melbadry9/enumsho
RUN go1.17 get -v github.com/cgboal/sonarsearch/cmd/crobat
RUN go1.17 get -v github.com/tomnomnom/assetfinder
RUN go1.17 get -v github.com/tomnomnom/httprobe
RUN go1.17 get -v github.com/melbadry9/subover
RUN go1.17 install github.com/OJ/gobuster/v3@latest
RUN go1.17 install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
RUN go1.17 install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
RUN go1.17 install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN GO111MODULE=on go1.17 get -v github.com/projectdiscovery/chaos-client/cmd/chaos

RUN wget --quiet https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux
RUN chmod +x findomain-linux
RUN mv findomain-linux ${GOPATH}/bin/findomain

RUN wget --quiet https://github.com/OWASP/Amass/releases/download/v3.15.2/amass_linux_amd64.zip
RUN unzip -j amass_linux_amd64.zip amass_linux_amd64/amass -d ${GOPATH}/bin/
RUN rm amass_linux_amd64.zip