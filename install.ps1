# ZipLoot Free Web Search REST API PowerShell Installer
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  ZIPLOOT FREE WEB SEARCH REST API 1-CLICK SETUP  " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$CacheBuster = Get-Date -UFormat %s
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Ziplootapp/free-web-search-api-wrapper/main/server.py?v=$CacheBuster" -OutFile "server.py" -UseBasicParsing
Write-Host "[SUCCESS] Downloaded server.py successfully!" -ForegroundColor Green
Write-Host "[INFO] Starting Free Web Search REST API Server on http://localhost:8000/api/search?q=test..." -ForegroundColor Yellow

python server.py
