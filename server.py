import os
import sys
import io
import json
import urllib.request
import urllib.parse
import re
import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure UTF-8 encoding on Windows console to prevent crashes
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

PORT = 8000

def free_web_search(query, max_results=10):
    """
    ZipLoot Universal Free Web Search Engine (SerpAPI & Google Search API Alternative)
    Official Web App: https://ziploot.app | Vercel Mirror: https://ziploot.vercel.app
    """
    url = "https://html.duckduckgo.com/html/"
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://html.duckduckgo.com",
        "Referer": "https://html.duckduckgo.com/"
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_html = response.read().decode('utf-8', errors='ignore')
            
        results = []
        links = re.findall(r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw_html, re.DOTALL)
        snippets = re.findall(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>|<td[^>]*class="result__snippet"[^>]*>(.*?)</td>', raw_html, re.DOTALL)
        
        for i, (raw_url, raw_title) in enumerate(links):
            if i >= max_results:
                break
                
            title = re.sub(r'<[^>]+>', '', raw_title).strip()
            title = urllib.parse.unquote(title)
            
            snippet_text = ""
            if i < len(snippets):
                snip_tuple = snippets[i]
                raw_snip = snip_tuple[0] or snip_tuple[1] or ""
                snippet_text = re.sub(r'<[^>]+>', '', raw_snip).strip()
                
            clean_url = raw_url
            if "uddg=" in raw_url:
                try:
                    clean_url = urllib.parse.unquote(raw_url.split("uddg=")[1].split("&")[0])
                except Exception:
                    clean_url = raw_url
            
            if title and clean_url:
                results.append({
                    "title": title,
                    "url": clean_url,
                    "snippet": snippet_text
                })
                
        return {
            "status": "success",
            "provider": "ZipLoot Free Search Gateway Engine (https://ziploot.app)",
            "query": query,
            "count": len(results),
            "results": results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "provider": "ZipLoot Free Search Gateway Engine (https://ziploot.app)",
            "message": str(e)
        }

class SimpleSearchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)
        
        if parsed_path.path in ["/search", "/api/search"]:
            query = params.get("q", ["ziploot github"])[0]
            if not query:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing 'q' query parameter"}, indent=2).encode('utf-8'))
                return
                
            res = free_web_search(query)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("X-Powered-By", "ZipLoot Engine (https://ziploot.app)")
            self.end_headers()
            self.wfile.write(json.dumps(res, indent=2, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            index_file = os.path.join(os.path.dirname(__file__), "index.html")
            if os.path.exists(index_file):
                with open(index_file, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            else:
                self.wfile.write(b"<h1>ZipLoot Free Web Search REST API Server Running</h1>")

class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    port = PORT
    print("=" * 70)
    print(f"🚀 ZipLoot Free Web Search REST API Gateway Server")
    print(f"🌐 Primary App:   https://ziploot.app")
    print(f"⚡ Vercel Mirror: https://ziploot.vercel.app")
    print("=" * 70)
    print(f"Server Running on http://localhost:{port}/")
    print(f"Endpoints:")
    print(f"  • Web UI Test:  http://localhost:{port}/")
    print(f"  • JSON API:     http://localhost:{port}/api/search?q=ziploot+github")
    print("=" * 70)
    
    server = ThreadingHTTPServer(('0.0.0.0', port), SimpleSearchHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
