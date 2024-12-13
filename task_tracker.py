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
        tasks = json.load(file)

    # Validate and fix missing fields
    for task in tasks:
        task.setdefault("createdAt", datetime.now().isoformat())
        task.setdefault("updatedAt", datetime.now().isoformat())
        task.setdefault("status", "todo")

    save_tasks(tasks)  # Save any fixed tasks back to the file
    return tasks


def list_tasks(status=None):
    tasks = load_tasks()

    # Filter tasks by status if specified
    if status:
        tasks = [task for task in tasks if task["status"] == status]

    # Check if there are tasks to display
    if not tasks:
        print("No tasks found.")
        return

    # Display tasks
    print(f"{'ID':<5}{'Description':<30}{'Status':<15}{'Created At':<25}{'Updated At':<25}")
    print("-" * 100)
    for task in tasks:
        print(f"{task['id']:<5}{task['description']:<30}{task['status']:<15}{task['createdAt']:<25}{task['updatedAt']:<25}")


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
        if len(args) == 1:
            list_tasks()  # List all tasks
        elif len(args) == 2:
            status = args[1]
            if status not in ["todo", "in-progress", "done"]:
                print("Error: Invalid status. Use 'todo', 'in-progress', or 'done'.")
            else:
                list_tasks(status)
        else:
            print("Error: Invalid usage. Use 'list' or 'list [status]'.")


if __name__ == "__main__":
    main()
