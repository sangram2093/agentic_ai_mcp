from google.adk.tools import FunctionTool
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.sessions import InMemorySessionService
import cx_Oracle
import os
from vertexai import init

# Initialize Gemini
init(project="your-gcp-project-id", location="us-central1")  # Replace with yours

# Oracle connection info from env
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASS = os.getenv("ORACLE_PASS")
ORACLE_HOST = os.getenv("ORACLE_HOST")
ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")

@FunctionTool
def run_oracle_sql(sql: str) -> list[dict]:
    """
    Executes a SELECT SQL query on Oracle and returns rows as a list of dicts.
    """
    dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE)
    conn = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PASS, dsn=dsn)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        return [dict(zip(cols, row)) for row in rows]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        cur.close()
        conn.close()

# Create the agent
oracle_agent = LlmAgent(
    name="oracle_query_agent",
    model="gemini-1.5-pro",
    description="Query Oracle data validation table",
    instruction="""
You are an expert in querying Oracle SQL. The table VALIDITY_RULES_RUN_STATE has these columns:
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

Use this to generate SQL for a user's question, then call the run_oracle_sql tool.
Only use SELECT queries. Do not include semicolons or comments.
""",
    tools=[run_oracle_sql],
    code_executor=BuiltInCodeExecutor(),
    session_service=InMemorySessionService()
)
