#!/bin/bash
echo "=================================================="
echo "  ZIPLOOT FREE WEB SEARCH REST API 1-CLICK SETUP  "
echo "=================================================="
curl -sL "https://raw.githubusercontent.com/Ziplootapp/free-web-search-api-wrapper/main/server.py" -o server.py
echo "[SUCCESS] Downloaded server.py successfully!"
python3 server.py
