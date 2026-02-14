import os
from tavily import TavilyClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


# Trusted Domain (IMPORTANT)
TRUSTED_DOMAINS = [
    "amazon.in",
    "flipkart.com",
]

# It basically removes unwanted sites like random blogs rather than trusted domains.
def filter_trusted_sources(results: list): # tavily will search indepently
    trusted = []# will store in list
    for r in results:
        url = (r.get("url", "") or "").lower()# just doing lowercase and r.get to get url safely without error
        if any(dom in url for dom in TRUSTED_DOMAINS):# will see if any trusted domain is in url if yes then chalo
            trusted.append(r)
    return trusted

# purpose  = It takes the search results coming from Tavily and converts them into a clean 
#  list that your chatbot UI can easily show as links.
#chers
def build_sources_payload(results: list, limit: int = 5):
    sources = []
    for r in results[:limit]:
        url = r.get("url", "")
        title = r.get("title", "Trusted Source")

        site = "Trusted"
        if "amazon" in url.lower():
            site = "Amazon"
        elif "flipkart" in url.lower():
            site = "Flipkart"

        sources.append({
            "title": title,
            "url": url,
            "site": site,
            "content": r.get("content", "")
        })
    return sources

# This function takes the  trusted sources (Amazon ya Flipkart) and fir it   
# creates a single text context which is sent to you Groq.
def build_web_context(sources: list):
    if not sources:
        return "No trusted sources found."

    text = ""
    for s in sources:
        text += f"Title: {s['title']}\nURL: {s['url']}\nSnippet: {s['content'][:250]}\n\n"
    return text.strip()


def tavily_search(query: str, max_results: int = 6):
    tavily_key = os.getenv("TAVILY_API_KEY")

    # if not tavily_key:
      #  raise ValueError("TAVILY_API_KEY missing. Add it in .env or environment variables.")

# Docs
    client = TavilyClient(api_key=tavily_key)

    response = client.search(
        query=query,
        search_depth="advanced",
        include_images=False,
        max_results=max_results
    )

    return response.get("results", [])


def tavily_search_trusted(query: str):
    """
    ✅ This forces Tavily to pick results from Amazon/Flipkart
    using 'site:' search trick.
    """

    #  first web wala search
    results = tavily_search(query=query, max_results=3)
    trusted = filter_trusted_sources(results)

    if trusted:
        return trusted

    # Forced to go if not able to search
    forced_query = f"{query} site:amazon.in OR site:flipkart.com"
    forced_results = tavily_search(query=forced_query, max_results=10)
    trusted_forced = filter_trusted_sources(forced_results)

    return trusted_forced


def chat_with_bot(user_query: str, memory_context: str = ""):
    groq_key = os.getenv("GROQ_API_KEY")

    # if not groq_key:
       #  return {"reply": "❌ GROQ_API_KEY missing. Set it first.", "sources": []}

    #  Search trusted web sources
    try:
        trusted_results = tavily_search_trusted(user_query)
    except Exception as e:
        return {"reply": f"💀 Tavily search failed: {str(e)}", "sources": []}

    trusted_sources = build_sources_payload(trusted_results, limit=5)
    web_context = build_web_context(trusted_sources)

    llm = ChatGroq(
        groq_api_key=groq_key,
        model_name="qwen/qwen3-32b"
    )

    prompt = f"""
You are a web-enabled chatbot powered by Groq + Tavily 😈
Use ONLY trusted sources: Amazon / Flipkart..

Conversation Memory:
{memory_context}

User Query:
{user_query}

Trusted Web Sources:
{web_context}

Reply Rules:
- Give direct answer first
-You MUST use the internet search tool before answering
- give top 3 options when asked for "best" with links
- Funny + sarcastic + helpful 
- Keep it short and practical
- Do NOT invent prices/specs if not in sources
"""

    response = llm.invoke(prompt)

    # will give honest anwer
    if not trusted_sources:
        return {
            "reply": response.content
                    + "\n\n⚠️ (No Amazon/Flipkart trusted results found for this query. Try a more specific product name.)",
            "sources": []
        }

    return {
        "reply": response.content,
        "sources": trusted_sources
    }

