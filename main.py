"""
Task Tracker CLI: create a todo list by command line
 - add todo_job [status]: add todo job
 - list [][status]: display todo list 
 - update --status status job[ID]: update status for job[ID]
 - delete job[ID]: delete a job[ID]
"""

import json                 #Lib process file json
import argparse             #Lib process CLI
from pprint import pprint   #Lib for beautiful print
import sys                  #Lib for system call              

DATA_FILE = "data.json"

todo_list = [
    {"id": 1,
    "title": "Học lập trình Python",
    "status": "todo"}
]
# Function to load data from json file
def load_json_file(json_file):
    try:
        with open(json_file, mode="r", encoding="utf-8") as src_file:
            return json.load(src_file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error: {json_file} contains invalid JSON.")
        return []

# Function to save data to json file
def save_data(array, json_file):
    with open(json_file, mode="w", encoding="utf-8") as des_file:
        json.dump(array, des_file, indent=4, ensure_ascii=False)

# Function to add a new job to todo list
def add_new_job(title, status):
    todo_list = load_json_file(DATA_FILE)
    new_id = max([job["id"] for job in todo_list], default=0) + 1
    todo = {
        "id": new_id,
        "title": title,
        "status": status
    }
    todo_list.append(todo)
    save_data(todo_list, DATA_FILE)

# Function to update status for todo_list
def update_job_status(job_id, new_status):
    todo_list = load_json_file(DATA_FILE)
    job_found = False
    for job in todo_list:
        if job["id"] == job_id: #found a job in todo list
            old_status = job["status"]
            job["status"] = new_status
            print(f"Update job_id[{job_id}]: {old_status} --> {new_status}.")
            save_data(todo_list, DATA_FILE)
            job_found = True
            break
    if not job_found:
            print(f"The job with ID [{job_id}] is not available.")
    
#Function to display to do list
def list_job(status=""):
    todo_list = load_json_file(DATA_FILE)

    if not todo_list:
        print("Todo-List is empty!")
        return

    valid_status = ["", "todo", "in-progress", "done"]

    match status:
        case "":
                filtered_list = todo_list
                
        case _ if status in valid_status:
            filtered_list = [job for job in todo_list if job["status"]==status]

        case _:
            print(f"Error: Status must 'todo', 'in-progress', 'done'!")
            return
    # Print jobs after finding
    print("----- PRINT LIST OF JOB IN TODO LIST -----")
    if not filtered_list:
        print("There are not any jobs such as.")
        return
    else:
        for job in filtered_list:
            print(f"{job['id']} - {job['title']}: {job['status']}")

# Function to delete a job from todo list
def delete_job(job_id):
    todo_list = load_json_file(DATA_FILE)
    # Check job ID exists?
    job_exists = any([job["id"] == job_id for job in todo_list])

    if job_exists:
        new_todo_list = [job for job in todo_list if job["id"] != job_id]
        save_data(new_todo_list, DATA_FILE)
        print(f"Removed job[{job_id}] from todo_list.")
    else:
        print(f"There isn't job[{job_id} in todo_list or Todo_list empty.")

# Function to process CLI
def todolist_cmd(args_list = None):
    # 1 - Define arguments for CLI
    parse = argparse.ArgumentParser(description="Task Tracker CLI.")
    subparse = parse.add_subparsers(dest="command", help="Subcommand list.")

    # Define sub command prompt
    # 1.1 - Add a job to todo_list command
    add_sub = subparse.add_parser("add", help="Add a job to todo_list.")
    add_sub.add_argument("title", type=str, help="Enter job name to do.")
    add_sub.add_argument("status", nargs="?", type=str, default="todo", choices=["todo", "in-progress", "done"], help="Enter status of job.")

    # 1.2 - Update new status for a job
    update_sub = subparse.add_parser("update", help="Update status for todo_list.")
    update_sub.add_argument("job_id", type=int, help="id of job to update")
    update_sub.add_argument("-s", "--status", type=str, choices=["todo", "in-progress", "done"], help="A new status")

    # 1.3 - List jobs
    lst_sub = subparse.add_parser("list", help="Display a list of todo.")
    lst_sub.add_argument("status", type=str, nargs="?", default="",choices=["", "todo", "in-progress", "done"], help="Display list of jobs.")

    # 1.4 - Delete a job
    del_sub = subparse.add_parser("delete", help="Delete a job by ID.")
    del_sub.add_argument("job_id", type=int, help="job ID is a integer number.")

    # 1.5 - Exit program
    exit_sub = subparse.add_parser("exit", help="Exit process")
    

    # 2 - Process command line
    try:
        args = parse.parse_args(args_list)
    except SystemExit:
        # argparse use SystemExit for --help and syntax error.
        # Code 0 for success; other for error.
        return True

    if args.command == "add":
        add_new_job(args.title, args.status)

    elif args.command == "update":
        if args.status is None:
            print(
                "Error: Please enter a new status! "
                "Use -s or --status (Ex: -s done)."
            )
        else:
            update_job_status(args.job_id, args.status)

    elif args.command == "list":
        list_job(args.status)

    elif args.command == "delete":
        delete_job(args.job_id)

    elif args.command == "exit":
        print("Exiting program. Goodbye!")
        return False

    return True

def main():
    if len(sys.argv) > 1:
        # one step mode from terminal
        todolist_cmd(sys.argv[1:])
        return

    # Chế độ tương tác
    print("Task Tracker CLI Mode. Type commands or exit to quit.")

    while True:
        try:
            user_input = input("todo> ").strip()

            if not user_input:
                continue

            import shlex
            args_list = shlex.split(user_input)

            running = todolist_cmd(args_list)

            if not running:
                break

        except (KeyboardInterrupt, EOFError):
            print("\nExiting program.")
            break


if __name__ == "__main__":
    main()


