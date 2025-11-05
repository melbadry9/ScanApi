# ScanApi 

## Installing

- Update `.env` __Database Configuration__.

### Docker 

```bash
docker compose up --build 
```
- Update `Enumeration/setting.py` __Tools Configuration__.

- Update `Enumeration/sources.py` __Active Tools__.


## Endpoints  

1. `/enum/active/<domain>/`
    - Start subdomain enumeration task in background then update DB using active tools
    - Domain ex: `example.com`

2. `/enum/passive/<domain>/`
    - Start subdomain enumeration task in background then update DB using passive tools
    - Domain ex: `example.com`

3. `/db/<domain>/`
    - Retrieve all subdomains from db if any exist

4. `/db/<domain>/?pro=http`
    - Retrieve subdomains with port 80 opened from DB if any exist

5. `/db/<domain>/?pro=https`
    - Retrieve subdomains with port 443 opened from DB if any exist

6. `/domain/info/<domain>/`
    - Retrieve domain information from DB
    - Domain ex: `example.com`

7. `/domain/delete/<domain>/`
    - Delete domain from DB
    - Domain ex: `example.com`

## Supported Tools

- [amass](https://github.com/OWASP/Amass)

- [findomain](https://github.com/Edu4rdSHL/findomain)

- [subfinder](https://github.com/projectdiscovery/subfinder)

- [gobuster](https://github.com/OJ/gobuster)

- [assetfinder](https://github.com/tomnomnom/assetfinder)

- [chaos](https://github.com/projectdiscovery/chaos-client)

- [aiodnsbrute](https://github.com/blark/aiodnsbrute)
