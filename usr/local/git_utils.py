import subprocess


jira_number = "CMS-63682"

def list_git_checkins(command, repo_path="/Users/manjunathmeti/git/cms-cmsp-splunk-platform/cms-cmsp-splunk-platform"):
    try:
        # Change to the repository directory 
        result = subprocess.run(
            command,
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Error running Git command: {e}")
        print(f"Stderr: {e.stderr}")
        return []

if __name__ == "__main__":
    # jira_number = input("Enter Jira number: ")
    # git log --grep='CMS-64382' --pretty=oneline
    command = ["git", "log", f"--grep={jira_number}" , "--pretty=format:%H"]
    checkins = list_git_checkins(command)
    if checkins:
        print("Git Check-ins for CMS-64382:")
        for commit in checkins:
            #print(commit)
            if commit:
                # git show --pretty="" --name-only bd61ad98 
                gs_command = ["git", "show", "--pretty=", "--name-only", commit]
                data = list_git_checkins(gs_command)
                print("\n".join(data))