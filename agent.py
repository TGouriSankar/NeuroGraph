from langchain_core.messages import HumanMessage
from config.env_loader import load_env
# load_env()
from graph.langgraph_workflow import run_graph
from llm.checker import check_output

def main():
    # Load environment variables
    load_env()

    # Send a message to the graph
    user_input = "Hi my name is Sankar and tell me about recent research paper about machine learning"
    response = run_graph([HumanMessage(content=user_input)])

    print("\n--- Agent Response ---")
    for m in response['messages']:
        m.pretty_print()

    # Optional: Run checker on a simple query
    print("\n--- Checker Output ---")
    print(check_output(user_input))

if __name__ == "__main__":
    main()
