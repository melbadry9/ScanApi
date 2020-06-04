FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential golang wget unzip git
EXPOSE 8000
COPY . /ScanApi 
WORKDIR /ScanApi
RUN pip3 install -r requirements.txt
RUN go get -u github.com/melbadry9/subover
RUN go get -u github.com/OJ/gobuster
RUN go get -u github.com/tomnomnom/assetfinder
RUN go get -u github.com/tomnomnom/httprobe
RUN go get -u -v github.com/projectdiscovery/subfinder/cmd/subfinder
RUN go get -u github.com/projectdiscovery/chaos-client/cmd/chaos
ENV GOROOT=/root/go GOPATH=/go PATH=/root/go/bin:$PATH
RUN wget https://github.com/OWASP/Amass/releases/download/v3.1.10/amass_v3.1.10_linux_amd64.zip
RUN wget https://github.com/Edu4rdSHL/findomain/releases/latest/download/findomain-linux
RUN chmod +x findomain-linux
COPY findomain-linux ${GOROOT}/bin/findomain
RUN unzip -j amass_v3.1.10_linux_amd64.zip amass_v3.1.10_linux_amd64/amass -d ${GOROOT}/bin/
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:Scan"]
