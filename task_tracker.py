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


def update_task(task_id, description=None, status=None):
    tasks = load_tasks()

    # Find the task with the given ID
    for task in tasks:
        if task["id"] == task_id:
            # Update description if provided
            if description:
                task["description"] = description

            # Update status if provided
            if status:
                if status not in ["todo", "in-progress", "done"]:
                    print("Error: Invalid status. Use 'todo', 'in-progress', or 'done'.")
                    return
                task["status"] = status

            # Update the updatedAt timestamp
            task["updatedAt"] = datetime.now().isoformat()

            # Save the tasks back to the file
            save_tasks(tasks)
            print(f"Task ID {task_id} updated successfully.")
            return

    # If task is not found
    print(f"Error: Task with ID {task_id} not found.")


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

    elif command == "update":
        if len(args) < 2:
            print("Error: Missing task ID")
            return
        try:
            task_id = int(args[1])
        except ValueError:
            print("Error: Task ID must be a number.")
            return

        # Parse optional arguments for description and status
        description = None
        status = None
        if "--description" in args:
            desc_index = args.index("--description") + 1
            if desc_index < len(args):
                description = " ".join(args[desc_index:])
            else:
                print("Error: Missing value for --description.")
                return

        if "--status" in args:
            status_index = args.index("--status") + 1
            if status_index < len(args):
                status = args[status_index]
            else:
                print("Error: Missing value for --status.")
                return

        update_task(task_id, description, status)


    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
