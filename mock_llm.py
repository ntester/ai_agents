class MockLLM:

    def decide_next_action(
        self,
        message: str,
        source: str = "user"
    ) -> dict:

        print("DEBUG SOURCE:", source)
        print("DEBUG MESSAGE:", message)

        message_lower = message.lower()

        # We searched the runbook.
        # We now have enough information to finish.
        if source == "runbook":
            return {
                "action": "finish",
                "answer": message
            }
        elif source == "airflow" and "source file was missing" in message_lower:
            return {
                "action": "check_s3_file",
                "file_path": "s3://customer-data/customers.csv"
            }

        elif source == "s3_bucket" and "file not found" in message_lower:
            return {
                "action": "query_snowflake",
                "sql": "SELECT COUNT(*) FROM customer_entity"
            }
        elif source == "s3_bucket":
            return {
                "action": "finish",
                "answer": (
                    "The expected file exists in S3, "
                    "so the Airflow failure may have another cause."
                )
            }
        elif source == "airflow" and (
                "snowflake" in message_lower
                or "row count" in message_lower
        ):
            return {
                "action": "query_snowflake",
                "sql": "SELECT COUNT(*) FROM customer_entity"
            }

        # We just received an Airflow result.
        # Search the runbook for what to do about it.
        elif source == "airflow":
            return {
                "action": "search_runbook",
                "topic": message
            }

        elif source == "snowflake":
            return {
                "action": "search_runbook",
                "topic": "missing source file"
            }

        # Original user request
        elif "customer_load" in message_lower:
            return {
                "action": "check_airflow_dag",
                "dag_name": "customer_load"
            }

        # Catch-all
        else:
            return {
                "action": "finish",
                "answer": "I don't know what else to investigate."
            }