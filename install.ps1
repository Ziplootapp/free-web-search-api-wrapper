# ZipLoot Free Web Search REST API PowerShell Installer
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  ZIPLOOT FREE WEB SEARCH REST API WEB DASHBOARD  " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$CacheBuster = Get-Date -UFormat %s
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Ziplootapp/free-web-search-api-wrapper/main/server.py?v=$CacheBuster" -OutFile "server.py" -UseBasicParsing
Write-Host "[SUCCESS] Downloaded interactive server.py successfully!" -ForegroundColor Green
Write-Host "[INFO] Opening ZipLoot Web Search API Dashboard in your browser on http://localhost:8000..." -ForegroundColor Yellow

python server.py
