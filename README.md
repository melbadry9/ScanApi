# ScanApi ![Python 3.5](https://img.shields.io/badge/Python-3.x-blue.svg) ![linux 64-bit](https://img.shields.io/badge/Linux-64bit-blue.svg) [![Total alerts](https://img.shields.io/lgtm/alerts/g/melbadry9/ScanApi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/melbadry9/ScanApi/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/melbadry9/ScanApi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/melbadry9/ScanApi/context:python)

Subdomains-enumeration, subdomain-takeover monitoring api and S3 bucket scanner.

## Installing

- Download and install

 ```bash
git clone https://github.com/melbadry9/ScanApi.git
cd ScanApi
sudo chmod 777 install.sh
./install.sh
```

- Update `ScanApi/setting.py` __Database Configuration__.

- Update `Enumeration/setting.py` __Tools Configuration__.

- Update `Enumeration/sources.py` __Active Tools__.

- Create database tables, admin and run server.

```bash
python3 manage.py makemigrations
python3 manage.py sqlmigrate Enumeration 0001
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Endpoints  

1. `/enum/active/<domain>/`
    - Start subdomain enumeration task in background then update db using active tools
    - Domain ex: `example.com`

2. `/enum/passive/<domain>/`
    - Start subdomain enumeration task in background then update db using passive tools
    - Domain ex: `example.com`

3. `/db/<domain>/`
    - Retrieve all subdomains from db if any exist

4. `/db/<domain>/?pro=http`
    - Retrieve subdomains with port 80 opened from db if any exist

5. `/db/<domain>/?pro=https`
    - Retrieve subdomains with port 443 opened from db if any exist

## Supported Tools

- [amass](https://github.com/OWASP/Amass)
- [gasset](https://github.com/melbadry9/gasset)
- [findomain](https://github.com/Edu4rdSHL/findomain)
- [subfinder](https://github.com/projectdiscovery/subfinder)
- [subover](https://github.com/melbadry9/SubOver)
- [sublist3r](https://github.com/melbadry9/Sublist3r)
- [httprobe](https://github.com/tomnomnom/httprobe)
- [gobuster](https://github.com/OJ/gobuster)
- [assetfinder](https://github.com/tomnomnom/assetfinder)
- [chaos](https://github.com/projectdiscovery/chaos-client)
- [enumsho](https://github.com/melbadry9/enumsho)
- [aiodnsbrute](https://github.com/blark/aiodnsbrute)
- [crobat](https://github.com/cgboal/sonarsearch)

## Donation

[![Coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://buymeacoffee.com/melbadry9)
