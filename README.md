# ScanApi ![Python 3.5](https://img.shields.io/badge/Python-3.x-blue.svg) ![linux 64-bit](https://img.shields.io/badge/Linux-64bit-blue.svg)

Subdomains-enumeration, subdomain-takeover monitoring api and S3 bucket scanner.

## Installing

- Linux

 ```bash
git clone https://github.com/melbadry9/ScanApi.git
cd ScanApi
sudo bash install.sh
python3 app.py
```

- Docker

```bash
docker build -t scanapi:latest .
docker run -d -p 8000:8000 scanapi
```

- Update `config.ini` before building docker image.

- Add slack hook in `config.ini` if Slack is Enabled.

- Commit docker image `docker commit <container id> scanapi:latest` to avoid losing data from db.

## Endpoints  

1. `/enum/domain/<domain>/`
    - Start subdomain enumeration task in background then update db
    - Domain ex: `example.com`

2. `/enum/s3/<bucket-name>/`
    - Start s3 bucket permissions scanner and update db
    - Bucket-name ex: `example-prod`

3. `/db/domain/<domain>/`
    - Retrieve all subdomains from db if any exist

4. `/db/domain/<domain>/?pro=http`
    - Retrieve subdomains with port 80 opened from db if any exist

5. `/db/domain/<domain>/?pro=https`
    - Retrieve subdomains with port 443 opened from db if any exist

6. `/db/s3/<bucket-name>/`
    - Retrieve s3 bucket scanner data from db if any exist

## Supported Tools

- [Amass](https://github.com/OWASP/Amass)
- [Gasset](https://github.com/melbadry9/gasset)
- [Subover](https://github.com/melbadry9/SubOver)
- [Sublist3r](https://github.com/melbadry9/Sublist3r)
- [Httprobe](https://github.com/tomnomnom/httprobe)
- [Gobuster](https://github.com/OJ/gobuster)
- [Assetfinder](https://github.com/tomnomnom/assetfinder)

## To-Do list

- [ ] Add directory brute forcing monitoring
- [ ] Add open ports monitoring
- [ ] Add scheduling jobs
- [ ] Add UI

## Donation

[![Coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://buymeacoffee.com/melbadry9)
