from fastmcp import tool, FastMCP
import cx_Oracle

@tool()
def run_oracle_sql(sql: str) -> list:
    dsn = cx_Oracle.makedsn("HOST", PORT, service_name="SERVICE")
    conn = cx_Oracle.connect(user="USERNAME", password="PASSWORD", dsn=dsn)
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

# MCP app start
if __name__ == "__main__":
    app = FastMCP(
        tools=[run_oracle_sql],
        transport="streamable-http",
    )
    app.serve(port=8080)
