import os, datetime, openai, json

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
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates README content from commit messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating README: {str(e)}"
    
"Counts amount of files in GitHub"
def count_files(project_path):
    file_count = 0
    exclude = {".git", ".github", ".vscode", ".devcontainer"}
    dir_names = []

    for root, dir, file, in os.walk(project_path):
        dir[:] = [d for d in dir if d not in exclude]
        dir_names.append(file)
        
        for f in file:
            if not f.startswith("."):
                file_count+=1

    return file_count, dir_names

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

'''
# Update readme based on ai output
def build_readme(commits): 
    res = generate_readme(commits)
    res = ""

    for commit in commits:
        commit_info = parse_commit(commit)
        c_type, c_content = commit_info["type"], commit_info["content"]
        res += f"{c_type}, {c_content}"
    
    return res
'''

        

if __name__ == "__main__":
    project_path = "."
    count, names = count_files(project_path)
    
    summary = (f"total files in repo: {count}\n" f"file names: {names}\n" f"last updated: {datetime.datetime.now()}")
    
    print(summary)

    # saves previous content
    with open("README.md", "r") as f:
        content = f.read()

    with open("README.md", "w") as f:
        f.write(content + "\n" + summary + "\n")

    sample_commits = [
    "feat: initialize SwiftUI project with base tab navigation",
    "feat: add Activity model and Core Data integration",
    "feat: implement AddActivityView with category selection",
    "fix: resolve crash when saving empty activity name",
    "refactor: extract ActivityFormView for reuse"
    ]      

    parsed_commit = parse_commits(sample_commits)
    
