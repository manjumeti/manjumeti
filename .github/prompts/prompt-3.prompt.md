Write a Python script using the GitHub REST API that does the following:

1. Inputs:
   - GitHub repository owner
   - Repository name
   - A search string to look for inside commit titles/messages
   - A GitHub personal access token
   - Search across all branches

2. Steps:
   - Fetch all branches in the repository.
   - For each branch, list all commits.
   - Filter commits where the commit message/title contains the input search string (case-insensitive).
   - For each matching commit, call the "Get a commit" API to retrieve the list of changed files.

3. Output:
   - For each matching commit, print:
     - Commit SHA
     - Commit message
     - Branch name
     - Three categorized lists of files:
         * Added files
         * Modified files
         * Removed files

4. Use `requests` library.
5. Handle GitHub pagination.
6. Organize code with reusable functions.
7. Print results in a clean structured format (JSON-like).
