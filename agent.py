import os
import cx_Oracle
from google.adk.tools import FunctionTool
from google.adk.agents import LlmAgent
from vertexai import init

# Initialize Gemini
init(project=os.environ["GOOGLE_CLOUD_PROJECT"], location="us-central1")

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
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

oracle_agent = LlmAgent(
    name="oracle_agent",
    model="gemini-2.5",  # or your available model
    instruction="""
You are an expert Oracle SQL generator. The table VALIDITY_RULES_RUN_STATE includes:
DATA_FEED_ID, RUN_DATE, DATA_RULE_NAME, CDE_NAME,
FEED_COUNT, DATA_RULE_VIOLATION_COUNT, DATA_RULE_VIOLATION_PERCENTAGE,
DATA_RULE_VIOLATION_DIST_VALUES, DATA_NULL_BLANK_COUNT, DATE_CREATED.

User will ask data questions. Generate safe SELECT query (no semicolons, only SELECT) and use the run_oracle_sql tool to execute.
""",
    tools=[run_oracle_sql]
)
