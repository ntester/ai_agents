# AI Agent Lab

This project is a small learning example that shows how an AI agent can investigate a data pipeline problem using tools, while an **agent harness** controls what the agent is allowed to do.

## How it works

The project currently uses a `MockLLM` instead of a real large language model. The mock simulates the decisions a real LLM would make by using simple Python `if/elif` rules.

The current investigation flow is:

```text
User question
    ↓
MockLLM decides what to check
    ↓
check_airflow_dag()
    ↓
Airflow reports a missing source file
    ↓
MockLLM decides to check S3
    ↓
check_s3_file()
    ↓
S3 confirms the file is missing
    ↓
MockLLM decides to check Snowflake
    ↓
query_snowflake()
    ↓
Snowflake shows the load is below normal
    ↓
MockLLM searches the runbook
    ↓
search_runbook()
    ↓
Final answer
```

## Project pieces

- **`mock_llm.py`** — simulates the reasoning and tool-selection decisions that a real LLM will eventually make.
- **`tools.py`** — contains deterministic Python tools such as Airflow, S3, Snowflake, log, and runbook checks.
- **`harness.py`** — provides safety and control around the agent. It tracks tool usage, limits the number of steps, allows only approved tools, and blocks unsafe Snowflake SQL.
- **`main.py`** — runs the agent loop, executes the selected tools, and feeds each result back to the mock LLM.
- **`test_harness.py`** — exercises the harness directly with safe and unsafe requests. These tests can later be converted to pytest unit tests.
- **`runbooks/`** — contains operational documentation that the agent can retrieve and use while investigating an incident.

## Why use an LLM?

The Python tools should continue to perform deterministic work such as querying Snowflake, checking S3, or retrieving logs.

A real LLM will eventually replace the hard-coded decision rules in `MockLLM`. Its job will be to interpret messy evidence, decide which tool is useful next, connect information from multiple systems, and produce a useful diagnosis.

The design principle is:

```text
LLM      = reasoning and judgment
Tools    = deterministic work
Harness  = safety, limits, and policy enforcement
```

The harness remains important even after a real LLM is added because the LLM should not be trusted to enforce its own safety rules.

## Current harness protections

The harness currently demonstrates:

- Maximum tool-call limits
- Approved-tool enforcement
- Snowflake read-only SQL validation
- Tool-call history for auditing

Example audit output:

```text
Steps: 4
Tool history:
  Tool: check_airflow_dag --> Input: customer_load
  Tool: check_s3_file --> Input: s3://customer-data/customers.csv
  Tool: query_snowflake --> Input: SELECT COUNT(*) FROM customer_entity
  Tool: search_runbook --> Input: missing source file
```

## Next steps

The next phase is to expand the harness tests, add more failure scenarios, and eventually replace `MockLLM` with a real LLM so that tool selection and incident reasoning are no longer hard-coded.
