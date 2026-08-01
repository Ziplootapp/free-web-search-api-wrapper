# ZipLoot 100% Free Web Search REST API Gateway (SerpAPI Alternative)
import json
import urllib.request
import urllib.parse
import re
import socketserver
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True

def perform_web_search(query):
    results = []
    
    # 1. Primary Engine: DuckDuckGo HTML / Lite Scraping
    try:
        url = "https://html.duckduckgo.com/html/"
        data = urllib.parse.urlencode({'q': query}).encode('utf-8')
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        pattern1 = r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>'
        pattern2 = r'<a[^>]+href="([^"]+)"[^>]*class="result__a"[^>]*>(.*?)</a>'
        matches = re.findall(pattern1, html, re.I | re.S) + re.findall(pattern2, html, re.I | re.S)
        snippets = re.findall(r'<(?:a|div)[^>]+class="result__snippet"[^>]*>(.*?)</(?:a|div)>', html, re.I | re.S)
        
        for i, m in enumerate(matches[:10]):
            link = m[0]
            title = m[1]
            
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            snippet_text = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else "ZipLoot Developer Platform & Free AI Utilities."
            
            if 'uddg=' in link:
                clean_url = urllib.parse.unquote(link.split('uddg=')[1].split('&')[0])
            else:
                clean_url = link
                
            results.append({
                "title": clean_title,
                "url": clean_url,
                "snippet": snippet_text
            })
    except Exception as e:
        print("[INFO] Engine 1 DDG HTML fallback:", e)

    # 2. Secondary Engine: Wikipedia Search API Fallback if Engine 1 returns empty
    if not results:
        try:
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
            req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for item in data.get('query', {}).get('search', [])[:10]:
                    clean_snippet = re.sub(r'<[^>]+>', '', item.get('snippet', '')).strip()
                    title = item.get('title', '')
                    clean_url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(title)
                    results.append({
                        "title": title,
                        "url": clean_url,
                        "snippet": clean_snippet
                    })
        except Exception as e:
            print("[INFO] Engine 2 Wiki API error:", e)

    return results

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZipLoot Free Web Search API (SerpAPI Alternative)</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #070b14; color: #f1f5f9; font-family: 'Inter', sans-serif; padding: 40px 20px; display: flex; justify-content: center; }
        .wrapper { max-width: 960px; width: 100%; }
        .header-title { font-size: 26px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .header-subtitle { color: #94a3b8; font-size: 15px; margin-bottom: 28px; }
        .search-bar-row { display: flex; gap: 12px; margin-bottom: 30px; }
        .search-input { flex: 1; background: #0f172a; border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; padding: 14px 18px; color: #fff; font-size: 15px; outline: none; transition: border 0.2s; }
        .search-input:focus { border-color: #6366f1; }
        .search-btn { background: #6366f1; color: #fff; border: none; padding: 0 28px; border-radius: 10px; font-weight: 700; font-size: 15px; cursor: pointer; transition: background 0.2s; }
        .search-btn:hover { background: #4f46e5; }
        .json-card { background: #0b1120; border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
        pre { font-family: 'Fira Code', monospace; font-size: 13.5px; line-height: 1.6; color: #38bdf8; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header-title">🚀 ZipLoot Free Web Search API (SerpAPI Alternative)</div>
        <div class="header-subtitle">Type a search query below to get instant structured JSON results without any API key!</div>
        
        <div class="search-bar-row">
            <input type="text" id="queryInput" class="search-input" value="ziploot vercel" placeholder="Type a search query..." onkeydown="if(event.key==='Enter') runSearch()">
            <button id="searchBtn" class="search-btn" onclick="runSearch()">Search API</button>
        </div>

        <div class="json-card">
            <pre id="jsonViewer">Loading live search API results...</pre>
        </div>
    </div>

    <script>
        async function runSearch() {
            var q = document.getElementById('queryInput').value.trim();
            if (!q) return;
            var viewer = document.getElementById('jsonViewer');
            viewer.innerText = '⚡ Fetching structured search API results for "' + q + '"...';
            
            try {
                var res = await fetch('/api/search?q=' + encodeURIComponent(q));
                var data = await res.json();
                viewer.innerText = JSON.stringify(data, null, 2);
            } catch (err) {
                viewer.innerText = JSON.stringify({ error: err.message }, null, 2);
            }
        }
        window.onload = runSearch;
    </script>
</body>
</html>"""

class SearchAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/api/search":
            params = urllib.parse.parse_qs(parsed_path.query)
            query = params.get("q", [""])[0]
            if not query:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Query parameter 'q' is required"}, indent=2).encode("utf-8"))
                return

            print(f"[INFO] Processing web search query: {query}")
            results = perform_web_search(query)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            response_payload = {
                "status": "success",
                "provider": "ZipLoot Free Search Gateway Engine",
                "query": query,
                "count": len(results),
                "results": results
            }
            self.wfile.write(json.dumps(response_payload, indent=2).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))

def run_server():
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), SearchAPIHandler)
    print(f"==================================================")
    print(f"  ZIPLOOT FREE WEB SEARCH REST API IS LIVE!       ")
    print(f"  Web Dashboard: http://localhost:{PORT}/")
    print(f"  API Endpoint:  http://localhost:{PORT}/api/search?q=ziploot+vercel")
    print(f"==================================================")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
