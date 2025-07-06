from fastmcp import FastMCP
import cx_Oracle

# Create FastMCP instance
mcp = FastMCP(name="OracleMCP")

@mcp.tool()
def run_oracle_sql(sql: str) -> list[dict]:
    """
    Execute a SELECT SQL query on Oracle and return results as a list of dicts.
    """
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

if __name__ == "__main__":
    # Run server over streamable HTTP on port 8080
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
