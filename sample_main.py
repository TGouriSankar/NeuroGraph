#  tools

from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper

api_wrapper_arxiv= ArxivAPIWrapper(top_k_results=2,doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv,description="Query arxiv papers")

# print(arxiv.invoke("dataset for traffic analysis"))

api_wrapper_wiki= WikipediaAPIWrapper(top_k_results=2,doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

# print(wiki.invoke("what is ml"))

from dotenv import load_dotenv
load_dotenv()

import os

os.environ['TAVILY_API_KEY']=os.getenv("TAVILY_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

from langchain_community.tools.tavily_search import TavilySearchResults

tavily = TavilySearchResults()

# print(tavily.invoke("Provide me the tafice video with more then 30mins youtube url or any dataset atlest give me 10 links"))

# combine the tools 
tools = [arxiv,wiki,tavily]

from langchain_groq import ChatGroq

llm=ChatGroq(model="qwen-qwq-32b")

# print(llm.invoke("What is ai"))

llm_with_tools = llm.bind_tools(tools=tools)

# Execute this call 
# print(llm_with_tools.invoke("hello"))





# https://www.youtube.com/watch?v=4Q3ut7vqD5o    "check this for video analysis project coding"





# Workflow
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage,HumanMessage # it will say human message or ai message
from typing import Annotated # labelling
from langgraph.graph.message import add_messages  
import graphviz

class State(TypedDict):
    messages : Annotated[list[AnyMessage], add_messages]

# entire chatbot with langGraph
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


# Node definition
def tool_calling_llm(state: State):
    return {"messages": [llm_with_tools.invoke(state['messages'])]} 

# build graph
builder = StateGraph(State)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

# Edgess
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm",tools_condition)
builder.add_edge("tools","tool_calling_llm")
# builder.add_edge("tools",END)


graph = builder.compile()
png_data = graph.get_graph().draw_mermaid_png()

# Save to a file
with open("output_diagram.png", "wb") as f:
    f.write(png_data)


# messages = graph.invoke({"message":HumanMessage(content="Hi")})
messages = graph.invoke({"messages":"Hi my name is sankar and tell me about recent research paper about machine learining"})
for m in messages['messages']:
    m.pretty_print()


from langchain.chains import LLMCheckerChain

# Assuming llm_with_tools is an instance of an LLM
checker_chain = LLMCheckerChain.from_llm(llm_with_tools)

# Then you can run the chain on some output
result = checker_chain.invoke("What is the capital of France?")
print(result)

