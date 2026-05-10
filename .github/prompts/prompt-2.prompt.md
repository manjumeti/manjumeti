Build a reusable Python class to connect to a JIRA instance and fetch issue details.

## Requirements:
1. Create a class-based JIRA client using the official Atlassian REST API (Cloud or Server).
2. Accept base_url, username/api_token, and optional session parameters.
3. Implement methods to:
   - Get details for a single JIRA issue by key (ex: "PROJ-123").
   - Get all child issues (subtasks or linked issues based on "parent" relationship).
   - Retrieve specific fields/attributes from each issue (inputs: list of field names).
   - Support pagination for JQL results.
4. Implement robust error handling:
   - HTTP error checks
   - Retry logic with exponential backoff (3–5 retries)
5. Output issue details as:
   - Python dict
   - Optionally save to JSON/CSV file using a helper method
6. Include usage examples at the bottom:
   - Fetch parent issue
   - Fetch all children
   - Extract specific attributes (ex: status, assignee.displayName, customfield_XXXXX)

## Notes:
- Use type hints
- Write clean, production-ready code
- Use requests library (not jira-python)
- Keep the code fully self-contained
