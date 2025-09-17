# Multi-Platform Docker Build and Deployment

This guide covers building Docker images for multiple platforms (macOS and Rocky Linux) and deploying them with custom certificates.

## Prerequisites

- Docker Desktop on macOS with BuildKit enabled
- Docker Hub account
- Rocky Linux server

## Building and Publishing Images

### Setup Multi-Platform Builder

```bash
# Create a new builder instance that supports multi-platform builds
docker buildx create --name multiplatform-builder --use

# Bootstrap the builder (downloads necessary components)
docker buildx inspect --bootstrap

# Verify the builder supports both platforms
docker buildx ls
```

### Build and Push Images

```bash
# Navigate to your project directory
cd /path/to/proposal_writer_agent

# Build and push Flask app for both platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f app/Dockerfile \
  -t mkprasad/mstg-proposal-app:1.0 \
  -t mkprasad/mstg-proposal-app:latest \
  --push \
  app/

# Build and push Nginx for both platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -f nginx/Dockerfile \
  -t mkprasad/mstg-proposal-nginx:1.0 \
  -t mkprasad/mstg-proposal-nginx:latest \
  --push \
  nginx/
```

### Verify Published Images

```bash
# Login to Docker Hub
docker login

# Verify images were pushed successfully
docker buildx imagetools inspect mkprasad/mstg-proposal-app:latest
docker buildx imagetools inspect mkprasad/mstg-proposal-nginx:latest
```

## Rocky Linux Deployment

### Install Docker on Rocky Linux

```bash
# Check if podman-docker is installed
rpm -qa | grep podman-docker

# If podman-docker exists, remove it and podman completely
sudo dnf remove -y podman-docker podman buildah skopeo crun

# Clean up leftover Podman configurations
sudo rm -rf /etc/containers/
sudo rm -rf ~/.config/containers/
sudo rm -rf /run/user/*/containers/
sudo rm -rf /run/user/*/podman/

# Remove any Podman environment variables
unset DOCKER_HOST
unset CONTAINER_HOST
unset CONTAINER_CONNECTION

# Update system
sudo dnf update -y

# Install Docker
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Check Docker daemon status
sudo systemctl status docker

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, then verify installation
docker --version
docker compose version
docker info
```

### Troubleshooting Docker Connection

```bash
# If you get connection errors after logout/login:

# 1. Check Docker daemon status
sudo systemctl status docker

# 2. Restart Docker daemon
sudo systemctl restart docker

# 3. Check for environment variables pointing to Podman
env | grep -i docker
env | grep -i container
env | grep -i podman

# 4. If any Podman-related variables exist, unset them:
unset DOCKER_HOST
unset CONTAINER_HOST
unset CONTAINER_CONNECTION

# 5. Test Docker connection
docker info

# 6. Ensure Docker socket has correct permissions
sudo chmod 666 /var/run/docker.sock
```

### Setup Application Directory

```bash
# Create application directory
mkdir -p ~/mstg-proposal-app
cd ~/mstg-proposal-app

# Create certs directory
mkdir -p certs

# Copy your certificates to the certs directory
cp /path/to/your/server.crt certs/
cp /path/to/your/server.key certs/

# Ensure proper permissions
chmod 600 certs/server.key
chmod 644 certs/server.crt
```

### Create Docker Compose File

Create `docker-compose.yml`:

```yaml
services:
  web:
    image: mkprasad/mstg-proposal-app:latest
    container_name: mstg-proposal-app-container
    restart: unless-stopped
    environment:
      - SECRET_KEY=${SECRET_KEY:-your-secret-key-here}
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: mkprasad/mstg-proposal-nginx:latest
    container_name: mstg-proposal-nginx-container
    restart: unless-stopped
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - web
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-k", "-f", "https://localhost/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  app-network:
    driver: bridge
```

### Deploy Application

```bash
# Pull the latest images
docker compose pull

# Start the application
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Test the application
curl -k https://localhost/healthz
curl -k https://localhost/
```

## Certificate Management

### Using Different Certificates

```bash
# Stop the application
docker compose down

# Replace certificates in certs/ directory
cp /path/to/new/server.crt certs/
cp /path/to/new/server.key certs/

# Update permissions
chmod 600 certs/server.key
chmod 644 certs/server.crt

# Restart with new certificates
docker compose up -d
```

### Using Let's Encrypt Certificates

```bash
# If you have Let's Encrypt certs (adjust paths as needed)
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem certs/server.crt
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem certs/server.key
sudo chown $USER:$USER certs/server.*
chmod 600 certs/server.key
chmod 644 certs/server.crt

# Restart application
docker compose restart nginx
```

## Environment Configuration

Create a `.env` file for environment variables:

```bash
# Create .env file
cat > .env << EOF
SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=production
GUNICORN_WORKERS=4
GUNICORN_THREADS=2
EOF

# Use environment file with compose
docker compose --env-file .env up -d
```

## Maintenance Commands

```bash
# Check container logs
docker compose logs nginx
docker compose logs web

# Execute into containers for debugging
docker compose exec web bash
docker compose exec nginx bash

# Check network connectivity
docker compose exec web curl -f http://localhost:8000/healthz
docker compose exec nginx curl -k https://localhost/healthz

# Restart specific service
docker compose restart nginx
docker compose restart web

# Full restart
docker compose down
docker compose up -d

# Update images
docker compose pull
docker compose up -d

# Clean up old images
docker image prune -f

# View resource usage
docker stats

# Backup certificates (recommended)
tar -czf certs-backup-$(date +%Y%m%d).tar.gz certs/
```

## Security Notes

1. Always use strong, unique SECRET_KEY values
2. Keep certificates secure with proper file permissions (600 for private keys)
3. Regularly update your Docker images for security patches
4. Monitor container logs for any security issues
5. Consider using Docker secrets for sensitive data in production



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