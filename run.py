from oracle_query_agent import oracle_agent

if __name__ == "__main__":
    question = input("Ask your data question: ")
    response = oracle_agent(user_input=question)
    print(response)
