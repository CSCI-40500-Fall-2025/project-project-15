# Project Description

This project provides a mechanism for autogenerating a changelog in the README file based on recent commit history. It utilizes the help of AI functionality to read repository commits and update the README file with key information such as the number of files, their names, and a timestamp for when the README was updated.

# Key Features

- **Autogenerating Changelog:** The project has a feature where the README autogenerates a changelog based on recent commit history.
- **AI Functionality:** The project uses AI to read repository commits and update the README file accordingly.
- **Github Actions Workflow:** The project includes a Github Actions workflow that is set up to automatically run on push.
- **Input Validation:** An input validation file was added to ensure the correct data is being entered.
- **Continuous Deployment Pipeline:** A snapshot build for the CD pipeline was added to the project.
- **GitHub Pages:** The project includes a live demo deployed onto GitHub Pages.

# Setup/Installation Instructions

Please note that the project requires a specific python version. 

1. Clone the repository from `github.com:CSCI-40500-Fall-2025/project-project-15`.
2. Uncomment the client.
3. Install the required Python version.

# Dependencies or Requirements

- Python
- GitHub account

# Usage Examples

Since the project is about autogenerating a README file, its main functionality is incorporated in the repository itself. As you make commits to the repository, the README file will update itself with a changelog based on your recent commit history.

# Additional Notes

- The project has a test suite for the `parse_commit` and `count_files` functions.
- The project's README file includes a layered software architecture.
- The main.yml file was temporarily disabled to not affect manual updates of the README.
- The project initially included a .gitignore and .env files, but these were later deleted.

---

total files in repo: 7
file names: [['test.py', 'VERSION', 'requirements.txt', 'example_file.py', '.gitignore', 'README.md', 'validation.py', 'prototype.py']]
last updated: 2025-11-12 04:07:11.875392
