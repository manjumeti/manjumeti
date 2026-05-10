import requests

# --- CONFIG ---
GITHUB_TOKEN = "ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # replace with your GitHub token
OWNER = "CXEPI"
REPO = "cms-cmsp-splunk-platform"
SEARCH_STRING = "CMS-46963"   # string to search in commit message

headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    'User-Agent': 'requests_error'
}


def get_all_branches(owner, repo):
    branches = []
    # https://api.github.com/repos/OWNER/REPO/branches
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"

    s = requests.Session()
    s.trust_env = False

    while url:
        r = s.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()

        for b in data:
            branches.append(b["name"])

        url = r.links.get("next", {}).get("url")

    return branches


def get_commits_in_branch(owner, repo, branch, search_string):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"sha": branch}
    matches = []

    while url:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        commits = r.json()

        for c in commits:
            message = c["commit"]["message"]
            if search_string.lower() in message.lower():
                sha = c["sha"]
                commit_details = get_commit_details(owner, repo, sha)
                matches.append(commit_details)

        url = r.links.get("next", {}).get("url")
        params = None

    return matches


def get_commit_details(owner, repo, sha):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()

    files = [f["filename"] for f in data.get("files", [])]

    return {
        "sha": data["sha"],
        "author": data["commit"]["author"]["name"],
        "date": data["commit"]["author"]["date"],
        "message": data["commit"]["message"],
        "files_changed": files
    }


# --- RUN ---
print("Fetching all branches...")
branches = get_all_branches(OWNER, REPO)

all_results = []

for br in branches:
    print(f"Checking branch: {br}")
    results = get_commits_in_branch(OWNER, REPO, br, SEARCH_STRING)
    all_results.extend(results)

# --- OUTPUT ---
for c in all_results:
    print("\n------------------------------")
    print(f"SHA: {c['sha']}")
    print(f"Author: {c['author']}")
    print(f"Date: {c['date']}")
    print("Message:", c["message"])
    print("Files affected:")
    for f in c["files_changed"]:
        print("  -", f)


