# ZipLoot 100% Free Web Search REST API Gateway (SerpAPI Alternative)
import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

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
                self.wfile.write(json.dumps({"error": "Query parameter 'q' is required"}).encode("utf-8"))
                return

            print(f"[INFO] Processing web search query: {query}")
            # DuckDuckGo HTML scraping
            search_url = "https://html.duckduckgo.com/html/"
            data = urllib.parse.urlencode({'q': query}).encode('utf-8')
            req = urllib.request.Request(search_url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, method="POST")

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    html = resp.read().decode('utf-8', errors='ignore')

                results = []
                from re import findall
                raw_results = findall(r'<a class="result__url" href="([^"]+)".*?<a class="result__snippet[^>]*>(.*?)</a>', html)
                
                for link, snippet in raw_results[:10]:
                    clean_snippet = snippet.replace('<b>', '').replace('</b>', '').strip()
                    results.append({"url": link.strip(), "snippet": clean_snippet})

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"query": query, "results": results}, indent=2).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>ZipLoot Free Web Search REST API is Live!</h1><p>Use /api/search?q=your+query</p>")

def run_server():
    httpd = HTTPServer(("0.0.0.0", PORT), SearchAPIHandler)
    print(f"==================================================")
    print(f"  ZIPLOOT FREE WEB SEARCH REST API IS LIVE!       ")
    print(f"  Endpoint: http://localhost:{PORT}/api/search?q=python")
    print(f"==================================================")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
