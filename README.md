
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/_KG6YNPd)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=20231659)

# Project 15

## Product Vision

FOR: developers or project builders that would like to have their projects Read Me updated and configured automatically

WHO: anyone working with a large codebase

The Write Me is a developer documentation automation tool

THAT automatically updates the Read Me based on the codebase

UNLIKE other Read Me generators

OUR PRODUCT continuously updates the Read Me throughtout the process

# Project Title

This project is a SwiftUI application designed to manage activities. It's based on SwiftUI and includes Core Data integration to allow for persistent storage. The app provides a tab-based navigation and features a model for activities. Users have the ability to add activities with category selection. 

## Key Features

- **Initialize SwiftUI project with base tab navigation**: This application is built using SwiftUI and offers a tab-based navigation interface.
- **Activity model and Core Data integration**: The application includes a structured Activity model and uses Core Data for persistent storage.
- **Implement AddActivityView with category selection**: Users can add different kinds of activities, with the possibility to select their category.
- **Resolve crash when saving empty activity name**: We've resolved an issue where the application would crash when trying to save an activity with an empty name.
- **Extract ActivityFormView for reuse**: The ActivityFormView component has been refactored for reusability throughout the application.

## Setup/Installation

*Note: This project was developed with SwiftUI, ensure that you have the latest version of Xcode installed on your machine before proceeding.*

1. Clone the repository to your local machine.
2. Open the project in Xcode.
3. Press Cmd + R to run the application on your preferred simulator.

## Dependencies

- SwiftUI
- Core Data

## Usage

After launching the application, you can navigate between different tabs. To add a new activity, click on the "+" button, fill out the form with the activity's details, and select the appropriate category. If you try to save an activity with an empty name, the app will prevent you from doing so to avoid crashes.

Remember, the changes you make are persistent thanks to Core Data integration, so you'll be able to see your added activities even after closing and reopening the app.

## Contributing

This is an open source project. We invite your feedback, bug reports, and pull requests.

## License

This project is licensed under the terms of the MIT license.
total files in repo: 4
file names: [['requirements.txt', 'README.md', '.gitignore', '.env', 'example_file.py', 'prototype.py']]
last updated: 2025-10-08 00:28:12.088981
