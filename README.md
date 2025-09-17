# Flask + Gunicorn + Nginx (HTTPS 443) — Dockerized

This project runs a Flask app behind Gunicorn and Nginx with TLS on port **443**.

## Structure
```text
flask-nginx-docker/
├─ app/
│  ├─ app.py
│  ├─ wsgi.py
│  ├─ requirements.txt
│  ├─ gunicorn.conf.py
│  └─ Dockerfile
├─ nginx/
│  ├─ nginx.conf
│  └─ Dockerfile
├─ certs/            # put server.crt and server.key here
├─ docker-compose.yml
└─ generate_dev_cert.sh
```

## Quickstart (dev, self-signed TLS)
```bash
cd flask-nginx-docker
./generate_dev_cert.sh
docker compose build
docker compose up -d
# Test:
curl -k https://localhost/       # -k to ignore self-signed cert
```

## Using real certificates
- Place your `server.crt` and `server.key` into `./certs/` and restart the stack:
  ```bash
  docker compose up -d --build
  ```
- For Let's Encrypt, terminate TLS on a public reverse proxy or run Certbot to get certs
  on the host, then mount them into `./certs`.

## Notes
- Gunicorn listens on `0.0.0.0:8000` inside the `app` container; Nginx proxies to it over the internal Docker network.
- Nginx exposes **443** on the host, so your entire app is served at `https://<host>:443/`.
- Health checks: `nginx` checks `/healthz`; `app` has `/healthz` too.
- Adjust worker counts, timeouts, and `client_max_body_size` per your workload.





## ============ Generating local certs ============
'''


#!/usr/bin/env bash
set -euo pipefail
CERT_DIR="${1:-./certs}"
mkdir -p "$CERT_DIR"
openssl req -x509 -newkey rsa:2048 -nodes -keyout "$CERT_DIR/server.key" -out "$CERT_DIR/server.crt" -days 365       -subj "/CN=localhost"
echo "Dev cert created at $CERT_DIR/server.crt and $CERT_DIR/server.key"



## ============ Rebuild sequence ============ 
docker compose down -v
docker compose build
docker compose up -d
curl -k https://localhost/healthz


## ============ nginx health ============
curl -k https://localhost/healthz

# app health from nginx path
curl -k https://localhost/

# logs
docker compose logs -f web
docker compose logs -f nginx


## ============ Troubleshooting ============
# 1) See why the app is failing healthcheck:
docker compose logs web

# 2) Shell into the app container and test from inside:
docker exec -it mstg-proposal-app-container sh
curl -f http://localhost:5000/healthz

# 3) Confirm Gunicorn is actually bound to 0.0.0.0:5000:
ss -lntp | grep 5000

# 4) If your app reads env/creds, verify they’re present:
env | sort
ls -l /app





## ============ Publish public image ============

docker login
docker compose build


docker build -t mkprasad/proposal-app:1.0 -f app/Dockerfile app
docker build -t mkprasad/proposal-nginx:1.0 -f nginx/Dockerfile nginx

docker tag mkprasad/proposal-app:1.0 mkprasad/proposal-app:latest
docker tag mkprasad/proposal-nginx:1.0 mkprasad/proposal-nginx:latest

docker push mkprasad/proposal-app:1.0
docker push mkprasad/proposal-app:latest
docker push mkprasad/proposal-nginx:1.0
docker push mkprasad/proposal-nginx:latest


```

