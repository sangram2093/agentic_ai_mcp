from oracle_query_agent import oracle_agent
from google.adk.runners import Runner

if __name__ == "__main__":
    print("Welcome to Oracle Data Validation Agent")
    runner = Runner(oracle_agent)
    while True:
        user_input = input("\nAsk a question (or type 'exit'): ")
        if user_input.lower() == "exit":
            break
        result = runner.run(user_input)
        print("\n=== Answer ===\n")
        print(result)
