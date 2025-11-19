# Project-15

Project-15 is a robust and dynamic project that leverages the power of AI to auto-generate a changelog based on recent commit history. It is containerized for easy deployment, and seamlessly integrates with your GitHub PRs. 

## Table of Contents
- [Setup Instructions](#setup-instructions)
- [Features](#features)
- [Usage](#usage)
- [Integrated Testing](#integrated-testing)
- [Continuous Deployment](#continuous-deployment)
- [Contributing](#contributing)

## Setup Instructions

To get started with Project-15, you need to set the `OPENAI_API_KEY`. This is a mandatory step and the project won't work if it is not set.

## Features

- **Auto-generate Changelog**: Project-15 has the functionality to read repository commits and auto-generate a changelog. This is a user feature that has been recently added and updated.

- **GitHub PR Integration**: The project now writes readme with existing content to the main branch instead of using GitHub API for PRs. 

- **Logging Mechanisms**: Added new logging mechanisms to assist with debugging.

- **AI Functionality**: This project employs AI to generate the README.

- **Containerization**: The application is containerized for easy deployment and scalability.

- **User Action Logic**: The user action logic has been updated to commit the readme code.

## Usage

The project comes with a prototype that writes the README file with the amount of files, the names of the files, and timestamp for when the README was updated. However, development is ongoing and some features are currently being tested.

## Integrated Testing

We have integrated a testing suite for `parse_commit` and `count_files`. The test workflow page has been updated and the test file has been revised. You can see the status of our tests on our GitHub Actions badge. 

## Continuous Deployment

Project-15 has enabled GitHub Pages and added a snapshot build for the continuous deployment pipeline. 

## Contributing

We are continually working on improving Project-15 and contributions are welcome. We recently moved `action.yml` to the proper actions directory and changed the Docker safe directory. We also updated the workflow name and fixed YAML indentation for users.

---

## Recent Updates

- Enabled GitHub Pages for live demo deployment.
- Removed outdated test links from README and updated test section link and badge.
- Changed Python version and uncommented the client.
- Updated version file with SNAPSHOT for testing release.
- Added PR integration, containerization, and landing page.
- Added logging mechanisms for better debugging. 

---

For more information on the recent commits and updates, refer to the commit history on our GitHub repository. We are always working on enhancing the project and making it more efficient. Your feedback and contributions are highly appreciated.

---

total files in repo: 13
file names: [['requirements.txt', 'Dockerfile', 'test.py', 'README.md', '.gitignore', 'VERSION', '.env', 'example_file.py', 'prototype.py', 'action.yml', 'validation.py'], ['index.html', 'styles.css', 'script.js', 'Logging.md']]
last updated: 2025-11-19 12:06:03.924313
