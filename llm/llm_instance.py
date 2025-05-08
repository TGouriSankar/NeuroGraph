from langchain_groq import ChatGroq
from tools.tool_setup import tools

# Load the model
llm = ChatGroq(model="qwen-qwq-32b")

# Bind tools
llm_with_tools = llm.bind_tools(tools=tools)
