import os
import datetime
import base64
import requests
import time
from openai import OpenAI
import git

_client = None

def get_openai_client():
    """Get or initialize OpenAI client (lazy initialization)"""
    global _client
    if _client is None:
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY must be set")
        _client = OpenAI(api_key=openai_key)
    return _client

def generate_readme(commits):
    """Generates README content based on commit messages"""
    commit_summary = "\n".join([f"- {commit}" for commit in commits])
    prompt = f"""
    Based on these commit messages, generate a clear and informative README.md content:

    {commit_summary}

    Please include:
    1. A brief project description
    2. Key features based on the commits
    3. Setup/installation instructions if applicable
    4. Dependencies or requirements
    5. Usage examples if relevant
    Format the response in proper Markdown.
    """
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates README content from commit messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating README: {str(e)}"

def count_files(project_path):
    """Counts amount of files in GitHub"""
    file_count = 0
    exclude = {".git", ".github", ".vscode", ".devcontainer", "venv", "env", "__pycache__", ".pytest_cache"}
    dir_names = []

    for root, dir, file, in os.walk(project_path):
        dir[:] = [d for d in dir if d not in exclude]
        dir_names.append(file)

        for f in file:
            if not f.startswith("."):
                file_count+=1

    return file_count, dir_names

def get_commits(repo_path=".", n=100):
    """Gets last n commits from git repo"""
    try:
        repo = git.Repo(repo_path)
        commits = []
        for commit in repo.iter_commits(max_count=n):
            commits.append(commit.message.strip().split('\n')[0])  # Get first line only
        return commits
    except Exception as e:
        print(f"Error accessing git repository: {str(e)}")
        return []

def parse_commit(commit): 
    """commits -> array of strings
    commits[i] = "<type>: <commit msg>"
    """
    if ":" in commit: 
        type_commit, content = commit.split(":", 1)
        type_commit = type_commit.strip()
        content = content.strip()
    else: 
        type_commit = "other"
        content = commit.strip() 

    return {
        "type": type_commit, 
        "content": content
    }

def create_pr_with_readme(readme_content, summary):
    """Creates a pull request with the updated README using GitHub API"""
    # Get GitHub token and repository info
    token = os.getenv("GITHUB_TOKEN") 
    repo = os.getenv("GITHUB_REPOSITORY")
    
    if not token or not repo:
        print("GitHub token or repository not found. Skipping PR creation.")
        return False
    
    api = "https://api.github.com"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        # Get default branch
        r = requests.get(f"{api}/repos/{repo}", headers=headers)
        r.raise_for_status()
        base_branch = r.json()["default_branch"]
        
        # Get branch SHA
        r = requests.get(f"{api}/repos/{repo}/git/ref/heads/{base_branch}", headers=headers)
        r.raise_for_status()
        sha = r.json()["object"]["sha"]
        
        # Create new branch
        branch = f"readme-update-{int(time.time())}"
        r = requests.post(
            f"{api}/repos/{repo}/git/refs",
            headers=headers,
            json={"ref": f"refs/heads/{branch}", "sha": sha}
        )
        r.raise_for_status()
        
        # Prepare README content with summary
        full_readme = f"{readme_content}\n\n---\n\n{summary}\n"
        
        # Base64 encoding is REQUIRED by GitHub Contents API
        content_b64 = base64.b64encode(full_readme.encode()).decode()
        
        # Update README on the new branch
        r = requests.put(
            f"{api}/repos/{repo}/contents/README.md",
            headers=headers,
            json={
                "message": "docs: auto-update README",
                "content": content_b64,
                "branch": branch
            }
        )
        r.raise_for_status()
        
        # Create PR
        r = requests.post(
            f"{api}/repos/{repo}/pulls",
            headers=headers,
            json={
                "title": "Auto-update README",
                "head": branch,
                "base": base_branch,
                "body": "Automatically generated README update based on recent commits."
            }
        )
        r.raise_for_status()
        pr_url = r.json()["html_url"]
        print(f"PR created: {pr_url}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating PR: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

if __name__ == "__main__":
    # Determine repo path (GitHub Actions uses /github/workspace, local uses .)
    repo_path = os.getenv("GITHUB_WORKSPACE") or "."
    project_path = repo_path
    
    count, names = count_files(project_path)
    summary = f"total files in repo: {count}\nfile names: {names}\nlast updated: {datetime.datetime.now()}"
    
    print(summary)
    
    # Get commits
    sample_commits = [
        "feat: initialize SwiftUI project with base tab navigation",
        "feat: add Activity model and Core Data integration",
        "feat: implement AddActivityView with category selection",
        "fix: resolve crash when saving empty activity name",
        "refactor: extract ActivityFormView for reuse"
    ]
    
    repo_commits = get_commits(repo_path)
    if repo_commits:
        print(f"Using repo commits: {repo_commits}")
        commits = repo_commits
    else:
        commits = sample_commits
    
    # Generate README content
    readme_content = generate_readme(commits)
    
    # Try to create PR, fallback to writing file locally if GitHub API not available
    pr_created = create_pr_with_readme(readme_content, summary)
    
    if not pr_created:
        # Fallback: write README locally (for local testing)
        print("Writing README.md locally (PR creation not available)")
        try:
            with open("README.md", "r") as f:
                existing_content = f.read()
        except FileNotFoundError:
            existing_content = ""
        
        with open("README.md", "w") as f:
            if existing_content and not existing_content.endswith('\n'):
                existing_content += '\n'
            f.write(f"{readme_content}\n\n---\n\n{summary}\n")
