import sys
import os
import json
from datetime import datetime

# Constants
TASKS_FILE = "tasks.json"

# Ensure the JSON file exists
def initialize_task_file():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)

# Load tasks from the file
def load_tasks():
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

# Save tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Main CLI logic
def main():
    initialize_task_file()
    args = sys.argv[1:]

    if not args:
        print("Usage: python task_tracker.py [command] [arguments]")
        return

    command = args[0]
    if command == "add":
        print("Add task logic here")
    elif command == "list":
        print("List tasks logic here")
    else:
        print("Unknown command: {command}")

if __name__ == "__main__":
    main()
