# Customer Load Runbook

## Missing Source File

If the customer_load DAG fails because the source file is missing:

1. Verify that the upstream partner delivered the file.
2. Check the expected S3 location.
3. Do not rerun the DAG until the file exists.
4. If the file is more than 2 hours late, contact the upstream support team.