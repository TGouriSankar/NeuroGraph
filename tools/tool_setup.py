from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
import os
from langchain_community.tools.tavily_search import TavilySearchResults

# Tool Setup
api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv, description="Query arxiv papers")

api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

# Ensure API key is loaded
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY is not set in environment variables.")

# Pass it directly
tavily = TavilySearchResults(tavily_api_key=tavily_api_key)

tools = [arxiv, wiki, tavily]

