import os
import datetime
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

def generate_readme(commits, existing_readme=""):
    """Generates README content based on commit messages"""
    commit_summary = "\n".join([f"- {commit}" for commit in commits])
    
    # Build the prompt with existing README context
    if existing_readme.strip():
        prompt = f"""
    Based on these recent commit messages, update the existing README.md content:

    Recent commits:
    {commit_summary}

    Existing README content:
    {existing_readme}

    Please:
    1. Preserve any important existing information (project description, setup instructions, etc.)
    2. Update or add new features based on the recent commits
    3. Maintain consistency in tone and structure
    4. Add new sections if the commits suggest new functionality
    5. Keep all existing sections that are still relevant
    Format the response in proper Markdown.
    """
    else:
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
            max_tokens=1200,
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
        # Fix git safe directory issue in containers
        import subprocess
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", repo_path], 
                      check=False, capture_output=True)
        
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
    
    # Read existing README to preserve content
    existing_readme = ""
    try:
        with open("README.md", "r") as f:
            content = f.read()
            # Extract just the README part (before the summary section)
            if "---" in content:
                existing_readme = content.split("---")[0].strip()
            else:
                existing_readme = content.strip()
    except FileNotFoundError:
        pass
    
    # Generate README content with context from existing README
    readme_content = generate_readme(commits, existing_readme)
    
    # Write README directly to file
    print("Writing updated README.md...")
    with open("README.md", "w") as f:
        f.write(f"{readme_content}\n\n---\n\n{summary}\n")
    
    print("README.md updated successfully!")
