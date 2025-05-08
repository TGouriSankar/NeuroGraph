from langchain.chains import LLMCheckerChain
from llm.llm_instance import llm_with_tools

# Build the LLM Checker Chain
checker_chain = LLMCheckerChain.from_llm(llm_with_tools)

def check_output(text: str):
    return checker_chain.invoke(text)
