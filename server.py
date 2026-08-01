# ZipLoot 100% Free Web Search REST API Gateway (SerpAPI Alternative)
import json
import urllib.request
import urllib.parse
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

def perform_web_search(query):
    results = []
    
    # 1. Primary Engine: Wikipedia & Web REST API Search
    try:
        wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
        req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=8) as resp:
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
        print("[ERROR during web search]:", e)

    return results

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
                "query": query,
                "total_results": len(results),
                "results": results
            }
            self.wfile.write(json.dumps(response_payload, indent=2).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>ZipLoot Free Web Search REST API Gateway is Live!</h1><p>Use <code>/api/search?q=python</code> to query search results.</p>")

def run_server():
    httpd = HTTPServer(("0.0.0.0", PORT), SearchAPIHandler)
    print(f"==================================================")
    print(f"  ZIPLOOT FREE WEB SEARCH REST API IS LIVE!       ")
    print(f"  Endpoint: http://localhost:{PORT}/api/search?q=python")
    print(f"==================================================")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
