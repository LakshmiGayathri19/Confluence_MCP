# main.py
from fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
import json

# === CONFIG ===
CONFLUENCE_URL = "{your_confluence_url}"
CONFLUENCE_SPACE_KEY = "{your_space_key}"
CONFLUENCE_API_USER = "{your_email}"
CONFLUENCE_API_TOKEN = "{your_api_token}"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

mcp = FastMCP("Confluence MCP")

def confluence_search(query: str):
    """Search Confluence and return a list of pages."""
    params = {
        "cql": f"siteSearch ~ '{query}' AND space = '{CONFLUENCE_SPACE_KEY}'",
        "limit": 5
    }
    response = requests.get(CONFLUENCE_URL, params=params, auth=(CONFLUENCE_API_USER, CONFLUENCE_API_TOKEN))
    response.raise_for_status()
    data = response.json()
    results = []
    for item in data.get("results", []):
        title = item.get("title")
        link = f"https://mock-data.atlassian.net/wiki{item['_links']['webui']}"
        results.append({"title": title, "url": link})
    return results

def fetch_page_content(url: str):
    """Fetch and extract text content from a Confluence page."""
    resp = requests.get(url, auth=(CONFLUENCE_API_USER, CONFLUENCE_API_TOKEN))
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.get_text(separator="\n")

def summarize_with_ollama(text: str) -> str:
    """Summarize text using Ollama."""
    payload = {
        "model": "tinyllama",
        "prompt": f"Summarize the following content in simple terms:\n\n{text}"
    }
    resp = requests.post(OLLAMA_API_URL, json=payload)
    resp.raise_for_status()
    return resp.json().get("response", "")

@mcp.tool()
def confluence_search_and_summarize(query: str) -> str:
    """Search Confluence space and summarize content from results."""
    search_results = confluence_search(query)
    summaries = []
    for result in search_results:
        try:
            content = fetch_page_content(result["url"])
            content = ' '.join(content.split())
            print(f"Fetched content for {result['title']} ({result['url']})")
            print(f"Content : {(content)}")
            summary = summarize_with_ollama(content[:100])
            summaries.append(f"**{result['title']}**\n{summary}\nURL: {result['url']}")
        except Exception as e:
            summaries.append(f"Failed to fetch {result['url']}: {e}")
    return "\n\n".join(summaries)

if __name__ == "__main__":
    mcp.run(transport="http", port=8080)
