#!/usr/bin/env bash
set -euo pipefail
CERT_DIR="${1:-./certs}"
mkdir -p "$CERT_DIR"
openssl req -x509 -newkey rsa:2048 -nodes -keyout "$CERT_DIR/server.key" -out "$CERT_DIR/server.crt" -days 365       -subj "/CN=localhost"
echo "Dev cert created at $CERT_DIR/server.crt and $CERT_DIR/server.key"
