import requests
from requests.auth import HTTPBasicAuth

# ------------------------------
# CONFIGURATION
# ------------------------------
JIRA_CLOUD_BASE_URL = "https://test.atlassian.net"  # Replace with your Jira Cloud URL
EMAIL = ""
API_TOKEN = ""
ISSUE_KEY = ""   # Example: ABC-101


auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}

# ------------------------------
# API ENDPOINT AND QUERY
# ------------------------------
search_url = f"{JIRA_CLOUD_BASE_URL}/rest/api/3/search/jql"

# For Jira Cloud, children of an Epic can be fetched via JQL:
#   "Epic Link" = EPIC-123     (Classic projects)
#
# For next-gen/team-managed projects:
#   parent = EPIC-123
#
# Use the one matching your setup.
jql_query = f'"Epic Link" = "{ISSUE_KEY}" ORDER BY created DESC'

payload = {
    "jql": jql_query,
    "fields": ["summary", "status", "issuetype", "parent"]
}

# ------------------------------
# CALL JIRA API
# ------------------------------
response = requests.post(
    search_url,
    json=payload,
    auth=auth,
    headers=headers
)

# ------------------------------
# PARSE RESULTS
# ------------------------------
if response.status_code == 200:
    data = response.json()
    print(data.keys())
    issues = data.get("issues", [])
    
    print(f"Found {len(issues)} child issues under epic {ISSUE_KEY}:")

    for issue in issues:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        status = issue["fields"]["status"]["name"]
        issue_type = issue["fields"]['issuetype']['name']
        print(f" - [{issue_type}]- {key}: {summary} [{status}]")
        
else:
    print("Error:", response.status_code, response.text)


# ---------------------------------------
# FETCH ISSUE DETAILS
# ---------------------------------------
issue_url = f"{JIRA_CLOUD_BASE_URL}/rest/api/3/issue/{ISSUE_KEY}?fields=*all"
resp = requests.get(issue_url, headers=headers, auth=auth)

if resp.status_code != 200:
    print("Error:", resp.status_code, resp.text)
    exit()

issue = resp.json()
print(issue['fields'].get('issues', []))
fields = issue["fields"]
issue_type = fields["issuetype"]["name"]

issue_links = fields.get("issuelinks", [])

print("Linked Work Items:")

if not issue_links:
    print("No linked work items found.")
else:
    for link in issue_links:
        link_type = link["type"]["name"]
        inward_desc = link["type"]["inward"]
        outward_desc = link["type"]["outward"]
        
        # Outward link (this → other issue)
        if "outwardIssue" in link:
            li = link["outwardIssue"]
            print(f"  - {ISSUE_KEY} {outward_desc} {li['key']}: {li['fields']['summary']} - {li['fields']['issuetype']['name']}")

        # Inward link (other → this issue)
        if "inwardIssue" in link:
            li = link["inwardIssue"]
            print(f"  - {ISSUE_KEY} {inward_desc} {li['key']}: {li['fields']['summary']} - {li['fields']['issuetype']['name']}")