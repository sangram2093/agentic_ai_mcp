import vertexai
from adk.type import Tool
from adk.dsl.agent import agent
from adk.dsl.steps import call, finish
from adk.dsl.tool import remote_tool
from vertexai.generative_models import GenerativeModel

# Init Gemini
vertexai.init(project="your-project-id", location="us-central1")
gemini_model = GenerativeModel("gemini-pro")

# Define the MCP tool
run_sql_tool = remote_tool(
    url="http://localhost:8080",  # Replace with Cloud Run URL later
    tool="run_oracle_sql",
    input_type="str",
    output_type="list[dict]"
)

@agent
def oracle_agent(user_input: str):
    # Step 1: Generate SQL
    prompt = f"""
You are a data analyst. The Oracle table VALIDITY_RULES_RUN_STATE has the columns:
- DATA_FEED_ID
- RUN_DATE
- DATA_RULE_NAME
- CDE_NAME
- FEED_COUNT
- DATA_RULE_VIOLATION_COUNT
- DATA_RULE_VIOLATION_PERCENTAGE
- DATA_RULE_VIOLATION_DIST_VALUES
- DATA_NULL_BLANK_COUNT
- DATE_CREATED

Write a SQL SELECT query (no semicolon, no comments) for this user request:
\"{user_input}\"
"""
    sql_response = gemini_model.generate_content(prompt)
    sql = sql_response.text.strip()
    print("\nGenerated SQL:\n", sql)

    # Step 2: Run the SQL using the MCP tool
    result = call(run_sql_tool, sql)

    # Step 3: Return the results
    finish(f"Query Result:\n{result}")
