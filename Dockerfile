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
ENV GOROOT=/root/go GOPATH=/go PATH=/root/go/bin:$PATH
RUN wget https://github.com/OWASP/Amass/releases/download/v3.0.27/amass_v3.0.27_linux_amd64.zip
RUN unzip -j amass_v3.0.27_linux_amd64.zip amass_v3.0.27_linux_amd64/amass -d ${GOROOT}/bin/
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:Scan"]
