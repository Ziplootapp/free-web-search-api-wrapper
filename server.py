# ZipLoot 100% Free Web Search REST API Gateway (SerpAPI Alternative)
import json
import urllib.request
import urllib.parse
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000

def perform_web_search(query):
    results = []
    
    # Engine 1: DuckDuckGo HTML / Lite Scraping
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
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        links = re.findall(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.I | re.S)
        snippets = re.findall(r'<(?:a|div)[^>]+class="result__snippet"[^>]*>(.*?)</(?:a|div)>', html, re.I | re.S)
        
        for i, (link, title) in enumerate(links[:10]):
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            snippet_text = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else "No snippet available."
            
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
        print("[INFO] Engine 1 fallback trigger:", e)

    # Engine 2: Wikipedia Search API Fallback if Engine 1 returns empty
    if not results:
        try:
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
            req = urllib.request.Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for item in data.get('query', {}).get('search', [])[:10]:
                    clean_snippet = re.sub(r'<[^>]+>', '', item.get('snippet', '')).strip()
                    results.append({
                        "title": item.get('title'),
                        "url': f"https://en.wikipedia.org/wiki/{urllib.parse.quote(item.get('title'))}",
                        "snippet": clean_snippet
                    })
        except Exception as e:
            print("[INFO] Engine 2 fallback trigger:", e)

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
