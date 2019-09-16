# ScanApi ![Python 3.5](https://img.shields.io/badge/Python-3.x-blue.svg) ![linux 64-bit](https://img.shields.io/badge/Linux-64bit-blue.svg)

Subdomains-enumeration and subdomain-takeover monitoring api.

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

- Add slack hook in `config.ini`

- For custom options edit `config.ini`

## Running  

- Open `http://127.0.0.1:8000/enum/example.com/` in your browser.

## Supported Tools

- [Amass](https://github.com/OWASP/Amass)
- [Gasset](https://github.com/melbadry9/gasset)
- [Subover](https://github.com/melbadry9/SubOver)
- [Sublist3r](https://github.com/melbadry9/Sublist3r)
- [Gobuster](https://github.com/OJ/gobuster)
- [Assetfinder](https://github.com/tomnomnom/assetfinder)

## To-Do list

- Add directory brute forcing monitoring.
- Add open ports monitoring.
- Add scheduling jobs.

## Donation

[![Coffee](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://buymeacoffee.com/melbadry9)