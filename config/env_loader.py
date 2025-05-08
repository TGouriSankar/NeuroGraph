from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

load_env()
