# main.py
from fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
import json
import re

# === CONFIG ===
CONFLUENCE_URL = "https://mock-data.atlassian.net/wiki/rest/api/content/search"
CONFLUENCE_SPACE_KEY = "~712020daed5d59750c4ded965c600b01a4cc45"
CONFLUENCE_API_USER = "lakshmi.gayathri.rangaraju@walmart.com"
CONFLUENCE_API_TOKEN = "ATATT3xFfGF0S3ulIxB3Aiu4zK8wBs5dOW4RVMT3IOR3KtJEJkIGQcybiqp4olr83Sbiivcxq2cefXMmAUoOLYdbVXaBI3AT8yLsEyUhb7slFeNisVPS0LmTtrPMCYNHqiZJGcJfOLERYN5zW4bhTLKa8rta-iA_Bvq4GI4vo12Mqlr-pxMgHp0=095DFBD4"  # Generate from Atlassian

OLLAMA_API_URL = "http://localhost:11434/api/chat"

mcp = FastMCP("Confluence MCP")

def remove_emojis(text: str) -> str:
    emoji_pattern = re.compile(
        "["                           # start of character class
        "\U0001F600-\U0001F64F"       # emoticons
        "\U0001F300-\U0001F5FF"       # symbols & pictographs
        "\U0001F680-\U0001F6FF"       # transport & map symbols
        "\U0001F1E0-\U0001F1FF"       # flags (iOS)
        "\U00002700-\U000027BF"       # dingbats
        "\U000024C2-\U0001F251"       # enclosed characters
        "\U0001F900-\U0001F9FF"       # supplemental symbols and pictographs
        "\U0001FA70-\U0001FAFF"       # extended symbols
        "\U00002600-\U000026FF"       # miscellaneous symbols
        "\U00002300-\U000023FF"       # misc technical
        "\U00002000-\U000020FF"       # general punctuation (optional, includes ZWJ/variation selectors)
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

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
        "model": "llama3",
        "messages": [{"role": "user", "content": f"Summarize this content:\n\n{text}"}],
        "stream": False  # important: disables streaming
    }
    resp = requests.post(OLLAMA_API_URL, json=payload)
    resp.raise_for_status()
    return resp.json().get("message", {}).get("content", "")

@mcp.tool()
def confluence_search_and_summarize(query: str) -> str:
    """Search Confluence space and summarize content from results."""
    search_results = confluence_search(query)
    summaries = []
    for result in search_results:
        try:
            content = fetch_page_content(result["url"])
            content = ' '.join(content.split())
            content = remove_emojis(content)
            print(f"Fetched content for {result['title']} ({result['url']})")
            print(f"Content : {(content)}")
            summary = summarize_with_ollama(content[:500])
            summaries.append(f"**{result['title']}**\n{summary}\nURL: {result['url']}")
        except Exception as e:
            summaries.append(f"Failed to fetch {result['url']}: {e}")
    return "\n\n".join(summaries)

if __name__ == "__main__":
    mcp.run(transport="http", port=8080)
