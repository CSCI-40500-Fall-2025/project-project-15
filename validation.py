import re
from pathlib import Path

# use regex to determine if a commit msg follows expected format 
# <type>:<msg>
def validate_commit_message(commit):
    if not commit or ":" not in commit:
        return False

    pattern = r"^[a-zA-Z]+:\s.+$"
    return bool(re.match(pattern, commit.strip()))

# make sure given path string is a valid path
def validate_directory_path(path_str):
    if not path_str or ":" in path_str or "//" in path_str:
        return False

    return Path(path_str).exists()
