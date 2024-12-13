# Task Tracker

A simple command-line interface (CLI) application to track and manage your tasks.

## Features
- Add, update, and delete tasks
- Mark tasks as `todo`, `in-progress`, or `done`
- List tasks by their status
- Persist tasks using a JSON file

## Usage
Run the script with the following commands:

```bash
python task_tracker.py add "Task description"
python task_tracker.py list
python task_tracker.py update [id] --description "Updated description" --status done
python task_tracker.py delete [id]


Requirements
Python 3.x