#!/bin/bash

set -e

echo "==> Starting XQuartz..."

open -a XQuartz

echo "==> Waiting for XQuartz..."
sleep 3

echo "==> Checking XQuartz..."

if ! lsof -nP -iTCP:6000 -sTCP:LISTEN | grep -q X11.bin; then
    echo "ERROR: XQuartz is not listening on TCP port 6000."
    echo "Make sure 'Allow connections from network clients' is enabled in:"
    echo "XQuartz → Settings → Security"
    exit 1
fi

echo "==> Getting current XQuartz authentication cookie..."

COOKIE=$(xauth list | awk '$1 ~ /\/unix:0$/ && $2=="MIT-MAGIC-COOKIE-1" {cookie=$3} END {print cookie}')

if [ -z "$COOKIE" ]; then
    echo "ERROR: Could not find an XQuartz MIT-MAGIC-COOKIE."
    exit 1
fi

echo "==> Using X11 cookie: $COOKIE"

echo "==> Updating X11 authorization for Docker..."

xauth add 192.168.65.254:0 MIT-MAGIC-COOKIE-1 "$COOKIE"

echo "==> X11 authorization configured."

echo "==> Starting EDAP20 Docker container..."

docker compose run base