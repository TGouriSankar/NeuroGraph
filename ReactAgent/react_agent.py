from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, TavilySearchResults
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

os.environ['TAVILY_API_KEY']=os.getenv("TAVILY_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Define the LLM
llm = ChatGroq(model="qwen-qwq-32b")

# Setup Tools
api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv, description="Query arxiv papers")

api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

tavily = TavilySearchResults()

tools = [arxiv, wiki, tavily]

llm_com = llm.bind_tools(tools)
# print(llm_com.invoke("Hi, can you tell me about the latest research on AI?"))

react_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate(
    template=react_template,
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
)

# Create the React Agent
agent = create_react_agent(llm, tools, prompt)

# Execute the agent with an example input 
from langchain.agents import AgentExecutor
agent_executes = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
response = agent_executes.invoke({"input": "Hi, can you tell me about the latest research on AI?"})

# Print the response
print(response)
