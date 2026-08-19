from pathlib import Path

def check_airflow_dag(dag_name: str) -> str:
    """
    Fake Airflow tool.
    """

    if dag_name == "customer_load":
        return (
            "DAG customer_load FAILED. "
            "Task load_customer_entity failed because "
            "the source file was missing."
        )

    return f"DAG {dag_name} completed successfully."

def search_runbook(topic: str) -> str:
    runbook_path = Path("runbooks/customer_load.md")

    if not runbook_path.exists():
        return "Runbook file was not found."

    contents = runbook_path.read_text()

    if "missing source file" in topic.lower():
        return contents

    return "No matching runbook entry found."

def check_s3_file(path: str) -> str:
    return "File not found in S3"


def query_snowflake(sql: str) -> str:
    """
    Fake Snowflake query tool.
    """

    sql_lower = sql.lower()

    if "customer_entity" in sql_lower:
        return (
            "Snowflake query result: "
            "customer_entity contains 42,000 rows for today's load. "
            "Normal daily volume is approximately 70,000 rows."
        )

    return "Snowflake query returned no matching data."


def get_recent_logs(service: str) -> str:
    return (
        "Recent logs show intermittent HTTP 503 errors "
        "from the upstream customer API."
    )