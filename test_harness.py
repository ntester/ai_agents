# Convert this to a real unit test later.
from harness import AgentHarness


def test_select_is_allowed():

    harness = AgentHarness(max_steps=5)

    harness.record_tool_call(
        "query_snowflake",
        "SELECT COUNT(*) FROM customer_entity"
    )

    print("SUCCESS: SELECT was allowed")


def test_delete_is_blocked():

    harness = AgentHarness(max_steps=5)

    try:
        harness.record_tool_call(
            "query_snowflake",
            "DELETE FROM customer_entity"
        )

        print("ERROR: DELETE was allowed!")

    except PermissionError as error:
        print("SUCCESS: Harness blocked DELETE")
        print(error)


def test_unknown_tool_is_blocked():

    harness = AgentHarness(max_steps=5)

    try:
        harness.record_tool_call(
            "delete_database",
            ""
        )

        print("ERROR: Unknown tool was allowed!")

    except PermissionError as error:
        print("SUCCESS: Harness blocked unknown tool")
        print(error)


def test_max_steps_is_enforced():

    harness = AgentHarness(max_steps=2)

    try:
        harness.record_tool_call(
            "check_airflow_dag",
            "customer_load"
        )

        harness.record_tool_call(
            "check_s3_file",
            "s3://customer-data/customers.csv"
        )

        # This is the third tool call.
        # max_steps is only 2.
        harness.record_tool_call(
            "search_runbook",
            "missing source file"
        )

        print("ERROR: Agent exceeded max steps!")

    except RuntimeError as error:
        print("SUCCESS: Harness stopped agent")
        print(error)


if __name__ == "__main__":

    print("\n===== TEST 1: SAFE SELECT =====")
    test_select_is_allowed()

    print("\n===== TEST 2: BLOCK DELETE =====")
    test_delete_is_blocked()

    print("\n===== TEST 3: BLOCK UNKNOWN TOOL =====")
    test_unknown_tool_is_blocked()

    print("\n===== TEST 4: MAX STEPS =====")
    test_max_steps_is_enforced()