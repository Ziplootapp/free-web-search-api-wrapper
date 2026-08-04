#!/bin/bash

echo "======================================================================"
echo "          ZipLoot Free Web Search REST API Gateway (1-Click)"
echo "          Official Web App: https://ziploot.app"
echo "          Vercel Mirror:   https://ziploot.vercel.app"
echo "======================================================================"
echo ""

if ! command -v python3 &> /dev/null
then
    echo "[ERROR] python3 could not be found. Please install Python 3.8+."
    exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Starting ZipLoot Search REST API Server on http://localhost:8000 ..."
python3 "$SCRIPT_DIR/server.py"
