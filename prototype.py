import os, datetime

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

