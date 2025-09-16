docker compose down -v
docker compose build
docker compose up -d
curl -k https://localhost/healthz
