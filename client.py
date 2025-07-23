import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8080/mcp/")  # Correct base endpoint
    query = input("Enter your query for Confluence: ")
    print("Calling MCP tool with query:", query)
    async with client:
        result = await client.call_tool("confluence_search_and_summarize", {"query": query})
        print("Response from MCP tool:\n", result)

if __name__ == "__main__":
    asyncio.run(main())
