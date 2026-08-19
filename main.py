from mock_llm import MockLLM
from harness import AgentHarness

from tools import (
    check_airflow_dag,
    search_runbook,
    check_s3_file,
    query_snowflake,
    get_recent_logs,
)

def run_agent(question: str):

    llm = MockLLM()
    harness = AgentHarness(max_steps=5)

    print("USER:")
    print(question)

    message = question
    source = "user"

    while True:

        print("\n--- NICOLE Agent thinking ---")

        decision = llm.decide_next_action(message, source)

        print("LLM DECISION:")
        print(decision)

        # -----------------------------------
        # Agent has finished
        # -----------------------------------
        if decision["action"] == "finish":

            print("\n========== NICOLE FINAL ANSWER ==========")
            print(decision["answer"])
            break

        # -----------------------------------
        # AIRFLOW TOOL
        # -----------------------------------
        elif decision["action"] == "check_airflow_dag":

            harness.record_tool_call(
                "check_airflow_dag",
                decision["dag_name"]
            )

            result = check_airflow_dag(
                decision["dag_name"]
            )

            print("\n========== NICOLE AIRFLOW TOOL RESULT ==========")
            print(result)

            # Feed result back to agent
            message = result
            source = "airflow"

        # -----------------------------------
        # S3 TOOL
        # -----------------------------------
        elif decision["action"] == "check_s3_file":

            harness.record_tool_call(
                "check_s3_file",
                decision["file_path"]
            )

            result = check_s3_file(
                decision["file_path"]
            )

            print("\n========== NICOLE S3 TOOL RESULT ==========")
            print(result)

            # Feed result back to agent
            message = result
            source = "s3_bucket"

        # -----------------------------------
        # SNOWFLAKE TOOL
        # -----------------------------------
        elif decision["action"] == "query_snowflake":

            harness.record_tool_call(
                "query_snowflake",
                decision["sql"]
            )

            result = query_snowflake(
                decision["sql"]
            )

            print("\n========== NICOLE SNOWFLAKE TOOL RESULT ==========")
            print(result)

            # Feed result back to agent
            message = result
            source = "snowflake"

        # -----------------------------------
        # RUNBOOK TOOL
        # -----------------------------------
        elif decision["action"] == "search_runbook":

            harness.record_tool_call(
                "search_runbook",
                decision["topic"]
            )

            result = search_runbook(
                decision["topic"]
            )

            print("\n========== NICOLE RUNBOOK TOOL RESULT ==========")
            print(result)

            # Feed result back to agent
            message = result
            source = "runbook"

        # -----------------------------------
        # LOG TOOL
        # -----------------------------------
        elif decision["action"] == "get_recent_logs":

            harness.record_tool_call(
                "get_recent_logs",
                decision["service_name"]
            )

            result = get_recent_logs(
                decision["service_name"]
            )

            print("\n========== NICOLE LOG TOOL RESULT ==========")
            print(result)

            # Feed result back to agent
            message = result
            source = "logs"

        # -----------------------------------
        # Unknown tool/action
        # -----------------------------------
        else:
            print("\nUNKNOWN ACTION:")
            print(decision["action"])
            break

    # -----------------------------------
    # Harness summary
    # -----------------------------------
    print("\n========== NICOLE HARNESS RESULTS ==========")
    print("Steps:", harness.steps)
    print("Tool history:")

    for tool_call in harness.tool_history:
        print(
            f"  Tool: {tool_call['tool']} "
            f"--> Input: {tool_call['input']}"
        )



def test_tools():

    print("\n=== AIRFLOW ===")
    print(check_airflow_dag("customer_load"))

    print("\n=== RUNBOOK ===")
    print(search_runbook("missing source file"))

    print("\n=== S3 ===")
    print(check_s3_file("s3://customer-data/customers.csv"))

    print("\n=== SNOWFLAKE ===")
    print(
        query_snowflake(
            "SELECT COUNT(*) FROM customer_entity"
        )
    )

    print("\n=== LOGS ===")
    print(get_recent_logs("customer-api"))

if __name__ == "__main__":
    #test_tools()
    run_agent(
        "The customer_load Airflow DAG failed last night. "
        "Can you investigate?"
    )