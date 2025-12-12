import os
import datetime
import logging
from logging import Logger, Handler
from typing import List, Tuple
import requests
import json

import git

try:
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover - surfaced during runtime if missing
    OpenAI = None  # type: ignore

try:
    from logtail import LogtailHandler  # type: ignore
except ImportError:
    LogtailHandler = None  # type: ignore


class BetterStackHandler(Handler):
    """Custom logging handler that sends logs to Better Stack using the direct API format."""
    
    def __init__(self, source_token: str, endpoint: str = "https://s1597068.eu-nbg-2.betterstackdata.com"):
        super().__init__()
        self.source_token = source_token
        self.endpoint = endpoint
        
    def emit(self, record):
        """Send log record to Better Stack."""
        try:
            # Format the log message
            log_entry = {
                "dt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                "message": self.format(record),
                "level": record.levelname,
                "logger": record.name
            }
            
            # Send to Better Stack
            response = requests.post(
                self.endpoint,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.source_token}"
                },
                json=log_entry,
                timeout=5
            )
            
            if response.status_code not in (200, 201, 204):
                # Silently fail to avoid log loops
                pass
        except Exception:
            # Silently fail to avoid log loops
            pass

_client = None
LOGGER_NAME = "readme_automation"


def configure_logging() -> Logger:
    """Configure project-wide logging with console + optional Logtail sinks."""
    log_level = os.getenv("LOG_LEVEL")
    if not log_level:
        log_level = "DEBUG" if os.getenv("CI") else "INFO"
    log_level = log_level.upper()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(log_level)
    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    source_token = os.getenv("LOGTAIL_SOURCE_TOKEN")
    ci_active = os.getenv("CI")
    if source_token and not ci_active:
        try:
            # Use custom BetterStackHandler that matches the working curl format
            betterstack_handler = BetterStackHandler(source_token=source_token)
            betterstack_handler.setLevel(log_level)
            betterstack_handler.setFormatter(formatter)
            logger.addHandler(betterstack_handler)
            logger.debug("Better Stack handler initialized for real-time monitoring.")
        except Exception as exc:
            logger.warning("Unable to attach Better Stack handler: %s", exc)
    elif ci_active:
        logger.debug("CI environment detected; external log streaming disabled.")

    logger.debug("Logger configured at %s level.", log_level)
    return logger


logger = configure_logging()

def get_openai_client():
    """Get or initialize OpenAI client (lazy initialization)"""
    global _client
    if OpenAI is None:
        raise ImportError("openai package is not installed; run `pip install openai`.")  # pragma: no cover
    if _client is None:
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            logger.critical("OPENAI_API_KEY is missing; cannot initialize OpenAI client.")
            raise ValueError("OPENAI_API_KEY must be set")
        logger.debug("Initializing new OpenAI client.")
        _client = OpenAI(api_key=openai_key)
    else:
        logger.debug("Reusing cached OpenAI client.")
    return _client

def generate_readme(commits, existing_readme=""):
    """Generates README content based on commit messages"""
    commit_summary = "\n".join([f"- {commit}" for commit in commits])
    logger.info("Generating README from %d commit(s).", len(commits))
    if existing_readme.strip():
        logger.debug("Existing README context detected (%d chars).", len(existing_readme))
    else:
        logger.debug("No existing README context provided.")
    
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
        logger.error("Error generating README content: %s", e)
        return f"Error generating README: {str(e)}"

def count_files(project_path) -> Tuple[int, List[List[str]]]:
    """Counts amount of files in GitHub"""
    logger.debug("Starting file count for %s.", project_path)
    file_count = 0
    exclude = {".git", ".github", ".vscode", ".devcontainer", "venv", "env", "__pycache__", ".pytest_cache"}
    dir_names = []

    for root, dir, file, in os.walk(project_path):
        dir[:] = [d for d in dir if d not in exclude]
        dir_names.append(file)

        for f in file:
            if not f.startswith("."):
                file_count+=1

    logger.info("File counting complete for %s: %d file(s) discovered.", project_path, file_count)
    return file_count, dir_names

def get_commits(repo_path=".", n=100):
    """Gets last n commits from git repo"""
    try:
        # Fix git safe directory issue in containers
        import subprocess
        subprocess.run(["git", "config", "--global", "--add", "safe.directory", repo_path], 
                      check=False, capture_output=True)
        
        logger.debug("Fetching up to %d commit(s) from %s.", n, repo_path)
        repo = git.Repo(repo_path)
        commits = []
        for commit in repo.iter_commits(max_count=n):
            commits.append(commit.message.strip().split('\n')[0])  # Get first line only
        logger.info("Retrieved %d commit(s) from repository.", len(commits))
        return commits
    except Exception as e:
        logger.error("Error accessing git repository: %s", e)
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

def generate_project_metadata(commits, file_count, file_names):
    """Generate structured project metadata using ML (Task #1 enhancement)"""
    commit_summary = "\n".join([f"- {commit}" for commit in commits[:20]])  # Limit for prompt size
    file_extensions = set()
    for file_list in file_names:
        for filename in file_list:
            if '.' in filename:
                ext = filename.split('.')[-1].lower()
                if ext not in ['md', 'txt', 'yml', 'yaml', 'json', 'gitignore']:
                    file_extensions.add(ext)
    
    file_info = f"Total files: {file_count}, Extensions: {', '.join(sorted(file_extensions)[:10])}"
    
    prompt = f"""Based on these commit messages and project structure, generate structured metadata in JSON format:

Commits:
{commit_summary}

Project structure: {file_info}

Return ONLY valid JSON with this exact structure:
{{
  "tags": ["tag1", "tag2", "tag3"],
  "category": "category name",
  "project_type": "type description",
  "tech_stack": ["tech1", "tech2"],
  "primary_language": "language",
  "description": "brief one-line description"
}}

Rules:
- tags: 3-5 relevant tags (lowercase, no spaces, use hyphens)
- category: one of: "web-app", "cli-tool", "library", "automation", "devops", "data-science", "other"
- project_type: brief description (e.g., "README automation tool", "API service")
- tech_stack: list of technologies used (e.g., ["Python", "GitHub Actions", "OpenAI"])
- primary_language: main programming language
- description: one sentence describing the project

Return ONLY the JSON, no markdown, no explanations."""

    try:
        start_time = datetime.datetime.now()
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates structured project metadata. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3,  # Lower temperature for more consistent structured output
        )
        
        latency_ms = int((datetime.datetime.now() - start_time).total_seconds() * 1000)
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()
        
        metadata = json.loads(content)
        metadata["ml_generated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        metadata["ml_model"] = "gpt-4"
        metadata["ml_latency_ms"] = latency_ms
        metadata["ml_status"] = "success"
        metadata["ml_prompt_version"] = "v1"
        
        logger.info("Generated project metadata successfully (latency: %d ms).", latency_ms)
        return metadata
        
    except json.JSONDecodeError as e:
        logger.error("Failed to parse ML metadata JSON: %s. Raw response: %s", e, content[:200])
        return {
            "tags": ["automation", "readme"],
            "category": "automation",
            "project_type": "README automation tool",
            "tech_stack": ["Python"],
            "primary_language": "Python",
            "description": "Auto-generates README from commit history",
            "ml_status": "failed",
            "ml_error": str(e),
            "ml_generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error("Error generating project metadata: %s", e)
        return {
            "tags": ["automation", "readme"],
            "category": "automation",
            "project_type": "README automation tool",
            "tech_stack": ["Python"],
            "primary_language": "Python",
            "description": "Auto-generates README from commit history",
            "ml_status": "failed",
            "ml_error": str(e),
            "ml_generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

def save_metadata(metadata, filepath="project_metadata.json"):
    """Save project metadata to JSON file"""
    try:
        # Read existing metadata if it exists to preserve history
        existing_metadata = {}
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    existing_metadata = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Add generation history
        if "generation_history" not in existing_metadata:
            existing_metadata["generation_history"] = []
        
        existing_metadata["generation_history"].append({
            "timestamp": metadata["ml_generated_at"],
            "metadata": metadata
        })
        
        # Keep only last 10 generations
        if len(existing_metadata["generation_history"]) > 10:
            existing_metadata["generation_history"] = existing_metadata["generation_history"][-10:]
        
        # Update current metadata
        existing_metadata.update({
            "tags": metadata.get("tags", []),
            "category": metadata.get("category", "other"),
            "project_type": metadata.get("project_type", ""),
            "tech_stack": metadata.get("tech_stack", []),
            "primary_language": metadata.get("primary_language", ""),
            "description": metadata.get("description", ""),
            "last_updated": metadata["ml_generated_at"],
            "ml_model": metadata.get("ml_model", ""),
            "ml_status": metadata.get("ml_status", "unknown")
        })
        
        with open(filepath, "w") as f:
            json.dump(existing_metadata, f, indent=2)
        
        logger.info("Saved project metadata to %s.", filepath)
        return True
    except Exception as e:
        logger.error("Error saving metadata: %s", e)
        return False

def auto_commit_changes(repo_path, files_to_commit, commit_message):
    """Auto-commit changes to git repository (Task #1: taking action)"""
    try:
        repo = git.Repo(repo_path)
        
        # Check if there are changes
        if repo.is_dirty() or repo.untracked_files:
            # Add files
            for file in files_to_commit:
                if os.path.exists(file):
                    repo.index.add([file])
                    logger.debug("Staged file: %s", file)
            
            # Create commit
            commit = repo.index.commit(commit_message)
            logger.info("Auto-committed changes: %s (commit: %s)", commit_message, commit.hexsha[:7])
            
            # Push if not in CI and AUTO_COMMIT is enabled
            if os.getenv("AUTO_COMMIT_PUSH") == "true" and not os.getenv("CI"):
                try:
                    origin = repo.remote("origin")
                    origin.push()
                    logger.info("Pushed changes to remote repository.")
                except Exception as e:
                    logger.warning("Could not push to remote: %s", e)
            
            return True, commit.hexsha
        else:
            logger.debug("No changes to commit.")
            return False, None
            
    except Exception as e:
        logger.error("Error auto-committing changes: %s", e)
        return False, None

def track_metrics(metadata, readme_success=True):
    """Track ML generation metrics"""
    metrics_file = "ml_metrics.json"
    
    try:
        metrics = {
            "total_generations": 0,
            "successful_generations": 0,
            "failed_generations": 0,
            "avg_latency_ms": 0,
            "last_updated": None
        }
        
        if os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                metrics = json.load(f)
        
        metrics["total_generations"] += 1
        if metadata.get("ml_status") == "success" and readme_success:
            metrics["successful_generations"] += 1
        else:
            metrics["failed_generations"] += 1
        
        # Update average latency
        if metadata.get("ml_latency_ms"):
            current_avg = metrics.get("avg_latency_ms", 0)
            total = metrics["total_generations"]
            new_latency = metadata["ml_latency_ms"]
            metrics["avg_latency_ms"] = int((current_avg * (total - 1) + new_latency) / total)
        
        metrics["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=2)
        
        logger.debug("Updated ML metrics: %d total, %d successful, avg latency: %d ms", 
                    metrics["total_generations"], metrics["successful_generations"], 
                    metrics["avg_latency_ms"])
        
    except Exception as e:
        logger.warning("Error tracking metrics: %s", e)

if __name__ == "__main__":
    # Determine repo path (GitHub Actions uses /github/workspace, local uses .)
    logger.info("Starting README automation run.")
    repo_path = os.getenv("GITHUB_WORKSPACE") or "."
    project_path = repo_path
    
    count, names = count_files(project_path)
    summary = f"total files in repo: {count}\nfile names: {names}\nlast updated: {datetime.datetime.now()}"
    
    logger.debug("Repository summary prepared:\n%s", summary)
    
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
        logger.info("Using %d repo commit(s) for README update.", len(repo_commits))
        commits = repo_commits
    else:
        logger.warning("No repo commits available; falling back to sample commits.")
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
    readme_start_time = datetime.datetime.now()
    readme_content = generate_readme(commits, existing_readme)
    readme_success = not readme_content.startswith("Error")
    
    # Generate structured project metadata (Task #1: Enhanced ML)
    logger.info("Generating structured project metadata using ML...")
    metadata = generate_project_metadata(commits, count, names)
    
    # Save metadata to file (Task #1: taking action - persisting ML output)
    metadata_saved = save_metadata(metadata)
    
    # Track metrics
    track_metrics(metadata, readme_success)
    
    # Write README directly to file
    logger.debug("Writing updated README.md with latest AI summary.")
    with open("README.md", "w") as f:
        f.write(f"{readme_content}\n\n---\n\n{summary}\n")
    
    # Add metadata section to README for visibility
    if metadata.get("ml_status") == "success":
        metadata_section = f"\n\n## Project Metadata (AI-Generated)\n\n"
        metadata_section += f"- **Category**: {metadata.get('category', 'N/A')}\n"
        metadata_section += f"- **Type**: {metadata.get('project_type', 'N/A')}\n"
        metadata_section += f"- **Tags**: {', '.join(metadata.get('tags', []))}\n"
        metadata_section += f"- **Tech Stack**: {', '.join(metadata.get('tech_stack', []))}\n"
        metadata_section += f"- **Primary Language**: {metadata.get('primary_language', 'N/A')}\n"
        metadata_section += f"- **Description**: {metadata.get('description', 'N/A')}\n"
        metadata_section += f"\n*Metadata generated by AI on {metadata.get('ml_generated_at', 'N/A')}*\n"
        
        # Insert before the --- separator
        readme_with_metadata = readme_content + metadata_section + f"\n---\n\n{summary}\n"
        with open("README.md", "w") as f:
            f.write(readme_with_metadata)
    
    logger.info("README.md updated successfully.")
    
    # Task #1: Auto-commit changes (taking action on behalf of user)
    if os.getenv("AUTO_COMMIT") != "false":  # Default to true unless explicitly disabled
        files_to_commit = ["README.md", "project_metadata.json"]
        commit_msg = f"docs: auto-update README and project metadata via ML\n\n- Generated metadata: {metadata.get('category', 'N/A')} project\n- Tags: {', '.join(metadata.get('tags', [])[:3])}\n- ML Status: {metadata.get('ml_status', 'unknown')}"
        
        committed, commit_sha = auto_commit_changes(repo_path, files_to_commit, commit_msg)
        if committed:
            logger.info("Successfully auto-committed ML-generated changes (commit: %s).", commit_sha[:7] if commit_sha else "N/A")
        else:
            logger.debug("Auto-commit skipped (no changes or disabled).")
    else:
        logger.debug("Auto-commit disabled via AUTO_COMMIT=false.")
