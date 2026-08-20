import os
from databricks import sql


#only allow queries that start with SELECT
def is_safe_query(query):
    return query.strip().upper().startswith("SELECT")


#run the query 
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
