import os, datetime, json
from dotenv import load_dotenv
from openai import OpenAI
import git

load_dotenv()

#Initialize oai client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"Generates README content based on commit messages"
def generate_readme(commits):
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


"Counts amount of files in GitHub"
def count_files(project_path):
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


"Gets last n commits from git repo"
def get_commits(repo_path=".", n=100):
    try:
        repo = git.Repo(repo_path)
        commits = []
        for commit in repo.iter_commits(max_count=n):
            commits.append(commit.message.strip().split('\n')[0])  # Get first line only
        return commits
    except Exception as e:
        print(f"Error accessing git repository: {str(e)}")
        return []

# commits -> array of strings
# commits[i] = "<type>: <commit msg>"
def parse_commit(commit): 
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
    project_path = "."
    count, names = count_files(project_path)

    summary = (f"total files in repo: {count}\n" f"file names: {names}\n" f"last updated: {datetime.datetime.now()}")

    print(summary)

    sample_commits = [
    "feat: initialize SwiftUI project with base tab navigation",
    "feat: add Activity model and Core Data integration",
    "feat: implement AddActivityView with category selection",
    "fix: resolve crash when saving empty activity name",
    "refactor: extract ActivityFormView for reuse"
    ]      

    repo_commits = get_commits(project_path)
    if repo_commits:
        print(f"Using repo commits: {repo_commits}")
        commits = repo_commits
    else:
        commits = sample_commits


    readme_content = generate_readme(commits)

    #check if README exists
    try:
        with open("README.md", "r") as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = ""

    #write new content (replace)
    with open("README.md", "w") as f:
        if existing_content and not existing_content.endswith('\n'):
            existing_content += '\n'
        f.write(f"{readme_content}\n\n---\n\n{summary}\n")

    #minor change


