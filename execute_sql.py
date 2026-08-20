"""
execute_sql.py (simplified)
------------------------------
Runs a SQL query safely against Databricks.

Simplified vs. the real version:
  - The "is this safe" check only does ONE thing: check it starts with
    SELECT. The real version also blocks dangerous keywords anywhere in
    the query, and checks for stacked/injected statements after a
    semicolon. Skipped here to keep the core idea clear: "only allow
    read-only queries."
  - No automatic LIMIT added if the query doesn't have one.
"""

import os
from databricks import sql


# ── The guardrail: only allow queries that start with SELECT ───────────────
def is_safe_query(query):
    return query.strip().upper().startswith("SELECT")


# ── Actually run the query ──────────────────────────────────────────────────
def execute_query(query):
    if not is_safe_query(query):
        raise ValueError(f"This query isn't allowed: {query}")

    connection = sql.connect(
        server_hostname=os.environ["DATABRICKS_HOST"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"]
    )
    cursor = connection.cursor()
    cursor.execute(query)

    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return columns, rows
