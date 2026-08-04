#!/usr/bin/env python3
"""
======================================================================
  ZipLoot Free Web Search REST API Gateway & Engine (v7.0)
  Official Web App: https://ziploot.app
  Vercel Mirror:   https://ziploot.vercel.app
======================================================================
  100% Free Google Search API & SerpAPI Alternative in Pure Python.
  Zero API Keys required, Zero rate limits, Zero external dependencies.
======================================================================
"""

import sys
import io
import os
import re
import json
import html
import urllib.request
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# Force UTF-8 encoding on Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

DEFAULT_PORT = 8000

def free_web_search(query):
    """
    Multi-Engine Web Search Scraper (DuckDuckGo, Wikipedia, & Smart Fallback)
    """
    results = []
    clean_query = query.strip()
    if not clean_query:
        return results

    # 1. Primary Engine: DuckDuckGo HTML Stream
    try:
        url = "https://html.duckduckgo.com/html/"
        data = urllib.parse.urlencode({'q': clean_query}).encode('utf-8')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://html.duckduckgo.com",
            "Referer": "https://html.duckduckgo.com/"
        }
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = resp.read().decode('utf-8', errors='ignore')

        matches = re.findall(r'<a\s+[^>]*class=["\']result__a["\'][^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', body, re.DOTALL | re.I)
        snippets = re.findall(r'<(?:a|td|div)\s+[^>]*class=["\']result__snippet["\'][^>]*>(.*?)</(?:a|td|div)>', body, re.DOTALL | re.I)

        for i, (raw_url, raw_title) in enumerate(matches[:12]):
            title = html.unescape(re.sub(r'<[^>]+>', '', raw_title)).strip()
            clean_url = raw_url
            if "uddg=" in raw_url:
                try:
                    clean_url = urllib.parse.unquote(raw_url.split("uddg=")[1].split("&")[0])
                except Exception:
                    pass
            snip = html.unescape(re.sub(r'<[^>]+>', '', snippets[i])).strip() if i < len(snippets) else ""

            if title and clean_url and not clean_url.startswith("https://duckduckgo.com"):
                results.append({
                    "title": title,
                    "url": clean_url,
                    "snippet": snip
                })
    except Exception as e:
        print(f"[DDG Engine Error]: {e}", file=sys.stderr)

    # 2. Secondary Fallback Engine: Wikipedia API
    if not results:
        try:
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(clean_query)}&format=json"
            w_headers = {"User-Agent": "ZipLootSearchBot/1.0 (https://ziploot.app; contact@ziploot.app)"}
            w_req = urllib.request.Request(wiki_url, headers=w_headers)
            with urllib.request.urlopen(w_req, timeout=6) as w_resp:
                w_data = json.loads(w_resp.read().decode('utf-8'))
                for item in w_data.get("query", {}).get("search", [])[:8]:
                    w_title = item.get("title", "")
                    w_snip = html.unescape(re.sub(r'<[^>]+>', '', item.get("snippet", "")))
                    w_link = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(w_title.replace(' ', '_'))}"
                    results.append({
                        "title": w_title,
                        "url": w_link,
                        "snippet": w_snip
                    })
        except Exception as e:
            print(f"[Wiki Engine Error]: {e}", file=sys.stderr)

    # 3. Tertiary Fallback Engine: Query Decomposition / Relaxation
    if not results:
        words = clean_query.split()
        if len(words) > 2:
            relaxed_query = " ".join(words[:3])
            print(f"[Query Relaxation]: Trying '{relaxed_query}'", file=sys.stderr)
            return free_web_search(relaxed_query)

    return results

class ZipLootSearchHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('X-Powered-By', 'ZipLoot Free Search Engine (https://ziploot.app)')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/search':
            params = urllib.parse.parse_qs(parsed.query)
            query = params.get('q', [''])[0].strip()

            if not query:
                self.send_response(400)
                self.send_cors_headers()
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                err_res = {
                    "status": "error",
                    "provider": "ZipLoot Free Search Gateway Engine (https://ziploot.app)",
                    "message": "Missing required query parameter 'q'. Example: /api/search?q=ziploot+github"
                }
                self.wfile.write(json.dumps(err_res, indent=2).encode('utf-8'))
                return

            results = free_web_search(query)

            self.send_response(200)
            self.send_cors_headers()
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            response_data = {
                "status": "success",
                "provider": "ZipLoot Free Search Gateway Engine (https://ziploot.app)",
                "official_website": "https://ziploot.app",
                "vercel_mirror": "https://ziploot.vercel.app",
                "query": query,
                "count": len(results),
                "results": results
            }
            self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
            return

        # Serve index.html as UI
        if path in ['/', '/index.html']:
            html_file = os.path.join(os.path.dirname(__file__), 'index.html')
            if os.path.exists(html_file):
                self.send_response(200)
                self.send_cors_headers()
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(html_file, 'rb') as f:
                    self.wfile.write(f.read())
                return

        self.send_response(404)
        self.send_cors_headers()
        self.end_headers()

def run_server():
    port = DEFAULT_PORT
    httpd = None
    
    # Smart Automatic Port Fallback (8000 -> 8001 -> 8002)
    for p in range(8000, 8010):
        try:
            httpd = HTTPServer(('', p), ZipLootSearchHandler)
            port = p
            break
        except OSError:
            continue

    if not httpd:
        print("[ERROR] Could not bind to any port in range 8000-8010. Please close existing servers.", file=sys.stderr)
        sys.exit(1)

    print("======================================================================")
    print("  🚀 ZipLoot Free Web Search REST API Gateway Server Running!")
    print(f"  ⚡ Local Web UI:   http://localhost:{port}/")
    print(f"  ⚡ API Endpoint:   http://localhost:{port}/api/search?q=ziploot+github")
    print("  🌐 Official Site:  https://ziploot.app")
    print("  ⚡ Vercel Mirror:  https://ziploot.vercel.app")
    print("======================================================================")

    try:
        webbrowser.open(f"http://localhost:{port}/")
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ZipLoot REST API Server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
