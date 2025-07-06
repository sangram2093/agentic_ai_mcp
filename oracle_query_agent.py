from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
import cx_Oracle
import os
from vertexai import init

# Initialize Gemini
init(project=os.environ["GOOGLE_CLOUD_PROJECT"], location="us-central1")

# Tool to run SQL on Oracle
@FunctionTool
def run_oracle_sql(sql: str) -> list[dict]:
    dsn = cx_Oracle.makedsn(
        os.environ["ORACLE_HOST"],
        os.environ.get("ORACLE_PORT", "1521"),
        service_name=os.environ["ORACLE_SERVICE"]
    )
    conn = cx_Oracle.connect(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASS"],
        dsn=dsn
    )
    try:
        cur = conn.cursor()
        cur.execute(sql)
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

# ADK agent
oracle_agent = LlmAgent(
    name="oracle_query_agent",
    model="gemini-1.5-pro",
    instruction="""
The Oracle table VALIDITY_RULES_RUN_STATE has the following columns:
- DATA_FEED_ID, RUN_DATE, DATA_RULE_NAME, CDE_NAME,
- FEED_COUNT, DATA_RULE_VIOLATION_COUNT, DATA_RULE_VIOLATION_PERCENTAGE,
- DATA_RULE_VIOLATION_DIST_VALUES, DATA_NULL_BLANK_COUNT, DATE_CREATED.

Generate SELECT queries only (no DELETE/INSERT/UPDATE, no semicolons).
Then call the run_oracle_sql tool to get results.
""",
    tools=[run_oracle_sql]
)
