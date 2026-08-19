class AgentHarness:

    def __init__(self, max_steps=5):

        self.max_steps = max_steps
        self.steps = 0

        self.tool_history = []

        self.allowed_tools = {
            "check_airflow_dag",
            "check_s3_file",
            "query_snowflake",
            "search_runbook",
            "get_recent_logs"
        }

    def record_tool_call(
        self,
        tool_name: str,
        tool_input: str = ""
    ):

        # -----------------------------------
        # RULE 1:
        # Is this an approved tool?
        # -----------------------------------

        if tool_name not in self.allowed_tools:
            raise PermissionError(
                f"Tool is not allowed: {tool_name}"
            )

        # -----------------------------------
        # RULE 2:
        # Don't let the agent run forever.
        # -----------------------------------

        self.steps += 1

        if self.steps > self.max_steps:
            raise RuntimeError(
                f"Agent exceeded maximum steps: "
                f"{self.max_steps}"
            )

        # -----------------------------------
        # RULE 3:
        # Snowflake is READ ONLY.
        # -----------------------------------

        if tool_name == "query_snowflake":

            sql = tool_input.strip().upper()

            if not sql.startswith("SELECT"):
                raise PermissionError(
                    "Snowflake query blocked. "
                    "Only SELECT statements are allowed."
                )

        # -----------------------------------
        # Record what happened
        # -----------------------------------

        self.tool_history.append(
            {
                "tool": tool_name,
                "input": tool_input
            }
        )