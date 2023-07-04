# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    if user.strip():  
        username, password = user.strip().split(';')
        username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# Function to register a new user
def reg_user():
    new_username = input("New Username: ")
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        return
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")

# Function to add a new task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    task_assigned_date = datetime.strptime(str(curr_date), DATETIME_STRING_FORMAT)
    task_completed = "No"
    task_list.append({'username': task_username, 'title': task_title, 'description': task_description,
                      'due_date': due_date_time, 'assigned_date': task_assigned_date, 'completed': task_completed})
    with open("tasks.txt", "a") as out_file:
        out_file.write(f"{task_username};{task_title};{task_description};{task_due_date};{curr_date};{task_completed}\n")
    print("Task added successfully")

# Function to view all tasks
def view_all():
    for i, task in enumerate(task_list, start=1):
        print(f"Task Number: {i}")
        print(f"Assigned to: {task['username']}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Due Date: {task['due_date']}")
        print(f"Assigned Date: {task['assigned_date']}")
        print(f"Completed: {task['completed']}")
        print()

# Function to view tasks assigned to the current user
def view_mine():
    username = curr_user
    user_tasks = [task for task in task_list if task['username'] == username]
    if len(user_tasks) == 0:
        print("No tasks assigned to you.")
        return
    print("Your Tasks:")
    for i, task in enumerate(user_tasks, start=1):
        print(f"Task Number: {i}")
        print(f"Title: {task['title']}")
        print(f"Description: {task['description']}")
        print(f"Due Date: {task['due_date']}")
        print(f"Assigned Date: {task['assigned_date']}")
        print(f"Completed: {task['completed']}")
        print()
    while True:
        try:
            task_choice = int(input("Enter the number of the task to select it, or -1 to return to the main menu: "))
            if task_choice == -1:
                return
            if task_choice < 1 or task_choice > len(user_tasks):
                print("Invalid task number. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    selected_task = user_tasks[task_choice - 1]
    print("1. Mark task as complete")
    print("2. Edit task")
    while True:
        try:
            task_option = int(input("Select an option: "))
            if task_option not in [1, 2]:
                print("Invalid option. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    if task_option == 1:
        if selected_task['completed']:
            print("Task is already marked as complete.")
        else:
            selected_task['completed'] = True
            with open("tasks.txt", "w") as out_file:
                for task in task_list:
                    task_completed = "Yes" if task['completed'] else "No"
                    out_file.write(f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{task_completed}\n")
            print("Task marked as complete.")
    elif task_option == 2:
        if selected_task['completed']:
            print("Task is already marked as complete. Editing is not allowed.")
        else:
            while True:
                edit_option = input("Enter 'u' to edit the username or 'd' to edit the due date: ")
                if edit_option not in ['u', 'd']:
                    print("Invalid option. Please try again.")
                    continue
                break
            if edit_option == 'u':
                new_username = input("Enter the new username: ")
                selected_task['username'] = new_username
            elif edit_option == 'd':
                while True:
                    try:
                        new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                        due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        break
                    except ValueError:
                        print("Invalid datetime format. Please use the format specified")
                selected_task['due_date'] = due_date_time
            with open("tasks.txt", "w") as out_file:
                for task in task_list:
                    task_completed = "Yes" if task['completed'] else "No"
                    out_file.write(f"{task['username']};{task['title']};{task['description']};{task['due_date'].strftime(DATETIME_STRING_FORMAT)};{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{task_completed}\n")
            print("Task edited successfully.")

# Function to generate task and user reports
def generate_reports():
    total_tasks = len(task_list)
    completed_tasks = sum([1 for task in task_list if task['completed']])
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum([1 for task in task_list if not task['completed'] and task['due_date'] < datetime.now()])
    incomplete_percentage = uncompleted_tasks / total_tasks * 100
    overdue_percentage = overdue_tasks / total_tasks * 100

    task_report = f"Total number of tasks: {total_tasks}\n" \
                  f"Total number of completed tasks: {completed_tasks}\n" \
                  f"Total number of uncompleted tasks: {uncompleted_tasks}\n" \
                  f"Total number of overdue tasks: {overdue_tasks}\n" \
                  f"Percentage of tasks that are incomplete: {incomplete_percentage}%\n" \
                  f"Percentage of tasks that are overdue: {overdue_percentage}%"

    user_report = f"Total number of users registered: {len(username_password)}\n" \
                  f"Total number of tasks: {total_tasks}\n"

    for username in username_password:
        user_tasks = [task for task in task_list if task['username'] == username]
        assigned_tasks = len(user_tasks)
        assigned_percentage = assigned_tasks / total_tasks * 100
        completed_assigned_tasks = sum([1 for task in user_tasks if task['completed']])
        completed_assigned_percentage = completed_assigned_tasks / assigned_tasks * 100
        incomplete_assigned_percentage = (assigned_tasks - completed_assigned_tasks) / assigned_tasks * 100
        overdue_assigned_tasks = sum([1 for task in user_tasks if not task['completed'] and task['due_date'] < datetime.now()])
        overdue_assigned_percentage = overdue_assigned_tasks / assigned_tasks * 100

        user_report += f"\nUsername: {username}\n" \
                       f"Total number of tasks assigned: {assigned_tasks}\n" \
                       f"Percentage of total tasks assigned: {assigned_percentage}%\n" \
                       f"Percentage of assigned tasks completed: {completed_assigned_percentage}%\n" \
                       f"Percentage of assigned tasks remaining: {incomplete_assigned_percentage}%\n" \
                       f"Percentage of assigned tasks overdue: {overdue_assigned_percentage}%"

    with open("task_overview.txt", "w") as task_report_file:
        task_report_file.write(task_report)

    with open("user_overview.txt", "w") as user_report_file:
        user_report_file.write(user_report)

# Function to display statistics
def display_statistics():
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    with open("task_overview.txt", "r") as task_report_file:
        task_report = task_report_file.read()
        print("Task Overview:")
        print(task_report)

    with open("user_overview.txt", "r") as user_report_file:
        user_report = user_report_file.read()
        print("\nUser Overview:")
        print(user_report)


# Main menu
while True:
    print("\nPlease select one of the following options:")
    print("r - Registering user")
    print("a - Add task")
    print("va - View all tasks")
    print("vm - View my tasks")
    print("gr - Generate reports")
    print("ds - Display statistics")
    print("e - Exit")

    option = input("Enter your option: ")

    if option == "r":
        reg_user()
    elif option == "a":
        add_task()
    elif option == "va":
        view_all()
    elif option == "vm":
        view_mine()
    elif option == "gr":
        generate_reports()
        print("Reports generated successfully.")
    elif option == "ds":
        display_statistics()
    elif option == "e":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")