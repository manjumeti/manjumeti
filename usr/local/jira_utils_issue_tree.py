import requests
from requests.auth import HTTPBasicAuth

# ---------------------------------------
# CONFIG
# ---------------------------------------
JIRA_CLOUD_BASE_URL = "https://test.atlassian.net"  # Replace with your Jira Cloud URL
EMAIL = ""
API_TOKEN = ""
ISSUE_KEY = ""   # Example: ABC-101

auth = HTTPBasicAuth(EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}


# =====================================================================
# RECURSIVE FUNCTION TO FETCH ISSUE + CHILDREN + LINKED ITEMS
# =====================================================================

def get_issue_tree(issue_key, visited=None):
    if visited is None:
        visited = set()

    # Avoid circular loops
    if issue_key in visited:
        return {"key": issue_key, "loop_detected": True}

    visited.add(issue_key)

    # -------- FETCH ISSUE DETAILS ----------
    issue_url = f"{JIRA_CLOUD_BASE_URL}/rest/api/3/issue/{issue_key}?fields=*all"
    resp = requests.get(issue_url, headers=headers, auth=auth)
    if resp.status_code != 200:
        return {"key": issue_key, "error": resp.text}

    issue = resp.json()
    fields = issue["fields"]
    issue_type = fields["issuetype"]["name"]

    node = {
        "key": issue_key,
        "type": issue_type,
        "summary": fields.get("summary", ""),
        "children": [],
        "linked_items": []
    }

    # =====================================================================
    # 1. GET CHILD ITEMS (RECURSIVE)
    # =====================================================================

    # ---------------- EPIC → Stories/Tasks ----------------
    if issue_type.lower() == "epic":
        jql = f'"Epic Link" = "{issue_key}"'
        search_url = f"{JIRA_CLOUD_BASE_URL}/rest/api/3/search"
        payload = {"jql": jql, "fields": ["summary", "issuetype", "status"], "maxResults": 200}

        search_resp = requests.post(search_url, json=payload, headers=headers, auth=auth)
        if search_resp.status_code == 200:
            for child in search_resp.json().get("issues", []):
                child_key = child["key"]
                node["children"].append(get_issue_tree(child_key, visited))

    # ---------------- STORIES/TASKS → Subtasks ----------------
    elif fields.get("subtasks"):
        for st in fields["subtasks"]:
            child_key = st["key"]
            node["children"].append(get_issue_tree(child_key, visited))

    # =====================================================================
    # 2. GET LINKED WORK ITEMS (NO RECURSION)
    # =====================================================================
    issue_links = fields.get("issuelinks", [])

    for link in issue_links:
        inward_desc = link["type"]["inward"]
        outward_desc = link["type"]["outward"]

        # outward
        if "outwardIssue" in link:
            li = link["outwardIssue"]
            node["linked_items"].append({
                "relation": outward_desc,
                "key": li["key"],
                "summary": li["fields"]["summary"],
            })

        # inward
        if "inwardIssue" in link:
            li = link["inwardIssue"]
            node["linked_items"].append({
                "relation": inward_desc,
                "key": li["key"],
                "summary": li["fields"]["summary"],
            })

    return node

# =====================================================================
# HELPER: PRETTY PRINT THE TREE
# =====================================================================

def print_tree(node, indent=0):
    prefix = " " * indent
    print(f"{prefix}- {node['key']} ({node['type']}): {node['summary']}")

    # print children
    for child in node.get("children", []):
        print_tree(child, indent + 4)

    # print linked items
    if node.get("linked_items"):
        print(" " * (indent + 2) + "Linked:")
        for l in node["linked_items"]:
            print(" " * (indent + 4) +
                  f"* {l['relation']} → {l['key']}: {l['summary']}")

root = get_issue_tree(ISSUE_KEY)
print_tree(root)