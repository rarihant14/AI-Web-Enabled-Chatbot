import os
# from tavily import TavilyClient
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()

client = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
print(client.invoke({"query": "Samsung S23 price in India", "max_results": 3}))