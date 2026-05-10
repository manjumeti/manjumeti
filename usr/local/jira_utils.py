from jira import JIRA

# ------------------------------
# CONFIG
# ------------------------------
JIRA_CLOUD_BASE_URL = "https://test.atlassian.net"  # Replace with your Jira Cloud URL
EMAIL = ""
API_TOKEN = ""
ISSUE_KEY = ""

# ------------------------------
# CONNECT TO JIRA CLOUD
# ------------------------------
jira = JIRA(
    server=JIRA_CLOUD_BASE_URL,
    basic_auth=(EMAIL, API_TOKEN)
)

# ------------------------------
# FETCH CHILD ISSUES OF EPIC
# ------------------------------
# For Company-Managed (Classic): "Epic Link" = EPIC
# For Team-Managed (Next-Gen): parent = EPIC
# Choose the one that matches your Jira project
jql = f'"Epic Link" = "{ISSUE_KEY}"'

issues = jira.search_issues(jql, maxResults=200)

print(f"Found {len(issues)} child issues under epic {ISSUE_KEY}:\n")

for issue in issues:
    print(f"- {issue.key} : {issue.fields.summary} [{issue.fields.status.name}]")


issue = jira.issue(ISSUE_KEY)

issue_type = issue.fields.issuetype.name
issue_type_id = issue.fields.issuetype.id

print(f"Issue: {ISSUE_KEY}")
print(f"Type: {issue_type} (ID: {issue_type_id})")
