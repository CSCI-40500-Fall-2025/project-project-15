# Project Title

This project is a helpful utility designed to simplify the process of maintaining a project's README file. It includes functionality to automatically generate a changelog derived from recent commit histories, and can also provide a summary of the repository, such as the number and names of files it contains, as well as the time when the README was last updated. This project utilizes the power of AI, specifically OpenAI, to enhance its capabilities.
This project is an innovative solution that helps in auto-generating your project's README file. It uses AI functionality to read your repository's commits and auto-generate a changelog based on recent commit history. Apart from this, it also provides a prototype that writes the README file with the amount of files, the names of the files, and timestamps for when the README was updated.

## Key Features

- **GitHub Actions Workflow**: Automatic execution of tasks upon push to the repository.
- **Repository Commit Reader**: A feature that reads the commit history of the repository.
- **OpenAI integration**: AI functionality to enhance the capabilities of the application.
- **README Generator**: A function that generates a comprehensive README file.
- **Auto-Changelog**: A user feature that automatically generates a changelog based on recent commit history.
- **Prototype**: Outputs the README file with the amount of files, the names of the files, and the timestamp for when the README was updated.


## Layered Software Architecture

## Important Qualities

**Determinism & Reproducibility:** Same input produces the same README unless commits have changed.  
**Low-ops / Zero servers:** Runs entirely in CI by default (GitHub Actions).  
**Security:** API keys are stored in repository or organization secrets.  
**Portability:** Local CLI mirrors CI steps with minimal vendor lock-in (LLM adapter).  
**Transparency:** Changelog is traceable to commits, and generated sections are fenced and tagged.

## Technologies Chosen

**Programming Language:** Python and/or Typescript (Node.js)
**Runtime Environment:** GitHub Actions runner (Ubuntu)  
**AI Integration:** OpenAI API (configurable through environment secrets)  
**Templating Engine:** Jinja for Markdown and changelog generation  
**Version Control & Hosting:** GitHub repository with GitHub App integration  
**Configuration Format:** YAML for flexible setup  
**Data Storage:** JSON artifact for single-repo state; S3/GCS for multi-repo state  
**Logging & Monitoring:** GitHub Actions logs with structured output and redaction  
**Testing Framework:** Pytest for unit and snapshot testing  
**Versioning Strategy:** Semantic Versioning (SemVer) for Action and bot releases

---

### 1) Interface Layer

**Interface:**  
GitHub Actions (primary), manual workflow dispatch, scheduled cron, optional CLI.

---

### 2) Auth & Access Layer

**GitHub:** GitHub application  
**AI Service:** API key via Actions secrets  
**Secret Hygiene:** OpenID Connect to cloud secret manager or GitHub encrypted secrets  
**Guardrails:** Per-repo allowlist, branch protection awareness, dry-run flag

---

### 3) Workflow Layer

**Coordinator:** A small runner script (Node/TypeScript or Python) that:  
- Parses inputs (branch, range of commits)  
- Calls domain services (commit collecting, summarization, generators)  
- Decides write-back mode (commit vs PR vs artifact only)  
- Handles resilience through retries or backoff

---

### 5) Integration Layer

**GitHub API Adapter:** Commits, tree/listing, contents read/write, PR comments, releases/tags  
**Formatter Adapters:** Markdown renderer, diff/highlight  


---

### 5) AI Integration Layer

**AI Adapter:** Centralized component for prompts, model choice, temperature, and token accounting
**Rate/Cost Controls:** Per-run token ceiling with fallbacks to template-only mode if exceeded

---

### 7) Data & Transaction Layer

**State Store (lightweight):**  
- Last successful run metadata (README hash, token usage)  
- Run logs and metrics  
- Can be a JSON artifact if mono-repo, or stored in S3/GCS if multi-repo  

**Atomic Updates:** Write to a temporary file, validate, then commit or open a PR to avoid force-push accidents

---

### 8) Observability Layer

**Logging:** Structured logs emitted in Actions with redaction for secrets and prompts  
**Alerts:** On failure, annotate the job and optionally create an issue label

---

### 10) Delivery Service

**Packaging:** Reusable GitHub Action (composite or JavaScript action) and Docker image for deterministic runs  
**Config:** YAML file with sections to manage, globs to scan, changelog style, and write mode  
**Versioning:** Semantic versioning (SemVer) for Action releases and a changelog for the bot itself

### Architecture Diagram

| **User Interface**              |
|---------------------------------|
| Scheduled Cron                  |
| Manual Pull Request             |
| CLI                             |
| GitHub Actions                  |

| **Auth and Access Service**     |
|---------------------------------|
| AI API Key                      |
| Repo-Allow List                 |
| Secret Key Storage              |
| File/Folder Path Whitelist      |

| **Workflow Service**            |
|---------------------------------|
| Commit Collection               |
| Commit Summarization            |
| README Generation               |
| Changelog Creation              |

| **AI Configuration Service**    |
|---------------------------------|
| AI Policy Configuration         |
| Rate/Cost Controls              |

| **Observability Service**       |
|---------------------------------|
| Failure/Success Alerts          |
| Logger                          |

| **Integration Service**         |
|---------------------------------|
| Commit Caching Service          |
| README Diff Creation            |
| Resilient Retry Service         |

| **Data Service** |
|---------------------------------|
| README State Collection Service |
| README Update                   |

| **Delivery Service** |
|---------------------------------|
| Packaging Service               |
| Configuration File Service      |
| Versioning Service              |

- Layered Software Architecture: Makes the project more organized and easier to manage.
- GitHub Actions Workflow: Automatically triggers a set of instructions (defined in the main.yml file) upon every push to the repository.
- AI Functionality: Reads repository commits and auto-generates a changelog.
- User Feature: Automatically generates a README file with the number of files, their names, and the timestamp of the last update.
- Online IDE: Ease of access and use from anywhere.

## Setup/Installation

1. Clone the repository to your local machine.
2. Delete the `.gitignore` and `.env` files if they exist in your local copy.
3. Please ensure you have the latest version of [OpenAI](https://beta.openai.com/) installed.
The project does not require any special setup or installation instructions. Just clone the repository and you are good to go.

## Dependencies

- [GitHub Actions](https://github.com/features/actions)
- [OpenAI](https://beta.openai.com/)

## Usage
- OpenAI: Used to provide Artificial Intelligence functionality.
- GitHub Actions: Required to set up the continuous integration/continuous delivery pipeline.

This tool is designed to be integrated directly into your existing Github workflow. Simply push your commits as normal, and the GitHub Actions workflow will automatically update your README file.
## Usage Examples

For detailed usage instructions, please refer to the commit titled "How to use prototype".
To use the auto-generating README feature, commit your changes with a descriptive message. The AI functionality will read the commit and update the README file accordingly.

---
To use the GitHub Actions workflow, push any changes to the repository. The actions defined in main.yml will automatically be triggered.

**Note**: An online IDE URL and deadline have been added to the project. Please refer to the latest commits for more information.
```bash
git commit -m "Descriptive commit message"
git push
```

## Updates
## Notes

Please refer to the commit history for the latest updates and bug fixes.
- The .gitignore and .env files have been deleted from the repository. Please make sure to set up your own according to your requirements.
- Don't forget to update the online IDE url and deadline according to your project timeline.
