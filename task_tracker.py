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

# Add tasks to file
def add_task(description):
    tasks = load_tasks()

    #Genereate a unique ID (incremental based on the last task's ID)
    task_id = max((task["id"] for task in tasks), default=0) + 1

    #Create a new task
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    # Add the new task to the list and save it
    tasks.append(new_task)
    save_tasks(tasks)

    print(f"Task added: {new_task['description']} (ID: {new_task['id']})")
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
        if len(args) < 2:
            print("Error: Missing task description.")
            return
        description = " ".join(args[1:])
        add_task(description)

    elif command == "list":
        print("List tasks logic here")
    else:
        print("Unknown command: {command}")

if __name__ == "__main__":
    main()
