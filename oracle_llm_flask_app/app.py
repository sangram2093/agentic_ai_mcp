
from flask import Flask, request, render_template, jsonify
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent
from vertexai import init
import json, os, cx_Oracle
from datetime import datetime

app = Flask(__name__)

# Init Gemini
init(project="cd-dev-t4vd-aag-001-1", location="europe-west3")

# Oracle tool
def run_oracle_sql(sql: str) -> str:
    dsn = "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCPS)(HOST=traag3u.cd.av.com)(PORT=1701)))(CONNECT_DATA=(SERVICE_NAME=traag3u_app.cd.av.com)))"
    conn = cx_Oracle.connect(user="trace_owner", password="xxxxx", dsn=dsn)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        if cur.description is None:
            return json.dumps({"error": "No results"})
        columns = [col[0] for col in cur.description]
        rows = [dict(zip(columns, r)) for r in cur.fetchall()]
        return json.dumps(rows, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        conn.close()

# Agent setup
oracle_agent = Agent(
    name="oracle_agent",
    model="gemini-1.5-pro-002",
    instruction="""
You are an Oracle SQL expert. The table DATA_VLD_RULE_RUN_STATE has columns:
 - FEED_ID, RUNDATETIME, RULE_NAME, FIELD_NAME, TOTAL_ROWS,
   RULE_VIOLATION_ROWS_COUNT, RULE_VIOLATION_ROWS_PERCENT,
   RULE_VIOLATION_DISTINCT_VALUES, NULL_OR_BLANK_COUNT, CREATED_AT.

When user asks a question, generate a SELECT-only SQL query.
Then call `run_oracle_sql` to get results.
""",
    tools=[run_oracle_sql]
)
runner = InMemoryRunner(agent=oracle_agent)
session = runner.session_service.create_session(app_name=runner.app_name, user_id="web")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")
    content = UserContent(parts=[Part(text=question)])
    raw_result, sql_text = None, None

    for event in runner.run(user_id=session.user_id, session_id=session.id, new_message=content):
        for part in event.content.parts:
            try:
                raw_result = json.loads(part.text)
            except:
                sql_text = part.text

    return jsonify({"data": raw_result, "message": sql_text})

if __name__ == "__main__":
    app.run(debug=True)
