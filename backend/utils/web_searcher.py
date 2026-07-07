import urllib.request
import urllib.parse
import re
from typing import List, Dict

class WebSearcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def search(self, query: str, num_results: int = 3) -> List[Dict[str, str]]:
        """Searches DuckDuckGo Lite interface using POST and returns titles, snippets, and links"""
        search_query = f"{query} ayurveda" if "ayurveda" not in query.lower() else query
        
        try:
            # Encode form data
            data = urllib.parse.urlencode({"q": search_query}).encode("utf-8")
            
            req = urllib.request.Request(
                "https://lite.duckduckgo.com/lite/",
                data=data,
                headers=self.headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                html = response.read().decode("utf-8", errors="replace")

            # Extract links and titles
            # class='result-link' or class="result-link"
            links_titles = re.findall(
                r'<a[^>]+href="([^"]+)"[^>]+class=[\'"]result-link[\'"][^>]*>(.*?)</a>',
                html,
                re.DOTALL
            )
            
            # Extract snippets
            # class='result-snippet' or class="result-snippet"
            snippets = re.findall(
                r'<td[^>]+class=[\'"]result-snippet[\'"][^>]*>\s*(.*?)\s*</td>',
                html,
                re.DOTALL
            )

            results = []
            for i in range(min(len(links_titles), len(snippets), num_results)):
                link = links_titles[i][0]
                title = links_titles[i][1]
                snippet = snippets[i]

                # Strip HTML tags and clean up entities
                title = self._clean_html(title)
                snippet = self._clean_html(snippet)

                # Unescape URL from DuckDuckGo redirect if present
                if "uddg=" in link:
                    parsed_url = urllib.parse.urlparse(link)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    if "uddg" in query_params:
                        link = query_params["uddg"][0]

                results.append({
                    "title": title.strip(),
                    "snippet": snippet.strip(),
                    "link": link.strip()
                })

            return results
        except Exception as e:
            print(f"Web search error: {str(e)}")
            return []

    def _clean_html(self, text: str) -> str:
        """Removes HTML tags and unescapes basic HTML entities"""
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace("&amp;", "&").replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">").replace("&#x27;", "'").replace("&#x2F;", "/")
        return text
