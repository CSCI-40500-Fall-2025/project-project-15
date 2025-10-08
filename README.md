# Project Title

This project is a handy tool designed to automate the generation of README.md files for your GitHub repositories. It leverages the power of AI and GitHub actions to create informative and up-to-date README files based on your recent commit history. The tool also includes a feature to generate a changelog and provides valuable information such as the number of files, their names, and the timestamp for when the README was updated.

## Key Features

- **GitHub Actions Workflow**: Automatically runs a workflow on every push to the repository.
- **Repository Commit Reader**: Reads the commit history of the repository to generate up-to-date README files.
- **AI Functionality**: Uses AI to generate informative README content based on commit messages.
- **Auto-generation of Changelog**: Creates a changelog based on recent commit history.
- **File Information**: The README includes the number of files, their names, and the timestamp for when the README was updated.

## Setup/Installation

To setup this tool in your project, please follow the steps given below:

1. Clone the repository.
2. Delete the .gitignore and .env files if they exist in your project directory.
3. Create a main.yml file in the .github/workflows directory.
4. Update the main.yml file with the necessary GitHub actions to run the workflow automatically on every push.

## Dependencies

This tool requires the following software to function properly:

- A GitHub account
- Access to GitHub actions

## Usage

To use this tool, make sure to follow the setup instructions provided above. Once done, every time you push to your repository, the GitHub action will trigger and update your README file with the latest commit information, including a changelog.

For example, if you've committed with the message "added new feature", your README will automatically update with this information under the changelog.

## Additional Information

This tool also includes a prototype that provides usage instructions and an online IDE URL and deadline if applicable.

Please note that this tool is currently in its prototype phase and may have some bugs. We're working hard to provide a smooth user experience.

---

total files in repo: 4
file names: [['requirements.txt', 'example_file.py', '.gitignore', 'README.md', 'prototype.py']]
last updated: 2025-10-08 16:22:44.465316
