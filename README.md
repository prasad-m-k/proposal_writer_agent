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


docker build -t mkprasad/mstg-proposal-app:1.0 -f app/Dockerfile app
docker build -t mkprasad/mstg-proposal-nginx:1.0 -f nginx/Dockerfile nginx

docker tag mkprasad/mstg-proposal-app:1.0 mkprasad/mstg-proposal-app:latest
docker tag mkprasad/mstg-proposal-nginx:1.0 mkprasad/mstg-proposal-nginx:latest

docker push mkprasad/mstg-proposal-app:1.0
docker push mkprasad/mstg-proposal-app:latest
docker push mkprasad/mstg-proposal-nginx:1.0
docker push mkprasad/mstg-proposal-nginx:latest


```


```
 # Troubleshooting 
```
```
1. Check the Dockerfile and Entrypoint Script
First, examine what's happening at line 47 of the docker-entrypoint.sh script:
bash# Pull the image and inspect it
docker pull mkprasad/mstg-proposal-nginx:latest

# Look at the entrypoint script
docker run --rm mkprasad/mstg-proposal-nginx:latest cat /docker-entrypoint.sh

2. Fix the Docker Run Command
The issue might be with the --replace flag placement. Try these alternatives:
bash# Option 1: Remove --replace (it's not a standard docker run flag)
docker run -d --name mstg-proposal-nginx \
  -e SECRET_KEY="${SECRET_KEY}" \
  mkprasad/mstg-proposal-nginx:latest --verbose

# Option 2: If you want to replace an existing container, remove it first
docker rm -f mstg-proposal-nginx 2>/dev/null || true
docker run -d --name mstg-proposal-nginx \
  -e SECRET_KEY="${SECRET_KEY}" \
  mkprasad/mstg-proposal-nginx:latest --verbose

# Option 3: Use --rm instead of --replace for temporary containers
docker run -d --rm --name mstg-proposal-nginx \
  -e SECRET_KEY="${SECRET_KEY}" \
  mkprasad/mstg-proposal-nginx:latest --verbose
3. Debug the Entrypoint Script
Run the container interactively to debug:
bash# Override the entrypoint to get a shell
docker run -it --rm \
  -e SECRET_KEY="${SECRET_KEY}" \
  --entrypoint /bin/bash \
  mkprasad/mstg-proposal-nginx:latest

# Then manually run the entrypoint script to see the error
/docker-entrypoint.sh --verbose
4. Common Fixes for Entrypoint Issues
The error suggests that line 47 in the entrypoint script is trying to execute a command with -- as an option. Common issues include:
Fix 1: Shell Script Issues
bash# If the script has Windows line endings, fix them:
docker run -it --rm --entrypoint /bin/bash mkprasad/mstg-proposal-nginx:latest
# Inside container:
sed -i 's/\r$//' /docker-entrypoint.sh
Fix 2: Argument Parsing Issues
The script might not be handling the --verbose argument correctly. Try without it:
bashdocker run -d --name mstg-proposal-nginx \
  -e SECRET_KEY="${SECRET_KEY}" \
  mkprasad/mstg-proposal-nginx:latest
5. Check Container Logs
If the container starts but fails quickly:
bashdocker logs mstg-proposal-nginx
6. Alternative Debugging Approach
Create a simple test without custom arguments:
bash# Basic run without any custom arguments
docker run -d --name mstg-proposal-nginx-test mkprasad/mstg-proposal-nginx:latest

# Check if it works
docker ps
docker logs mstg-proposal-nginx-test

7. Port Mapping (if needed)
Since this appears to be an nginx container, you might also need port mapping:
bashdocker run -d --name mstg-proposal-nginx \
  -p 80:80 -p 443:443 \
  -e SECRET_KEY="${SECRET_KEY}" \
  mkprasad/mstg-proposal-nginx:latest
The most likely solution is removing the --replace flag and ensuring the --verbose argument is supported by the entrypoint script. If you need to replace an existing container, explicitly remove it first with docker rm -f mstg-proposal-nginx.RetryClaude does not have the ability to run the code it generates yet.
```