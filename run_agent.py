from oracle_query_agent import oracle_agent

if __name__ == "__main__":
    while True:
        user_input = input("\nAsk a data question (or 'exit'): ")
        if user_input.lower() == "exit":
            break
        response = oracle_agent(user_input)
        print("\n🔎 Answer:\n", response)
