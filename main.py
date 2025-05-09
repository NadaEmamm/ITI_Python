import os
import re
import json
import hashlib

logged_in_user = None
USER_FILE = 'users.json'
PROJECT_FILE = 'projects.json'

#PROJECTS
###########################
def load_projects():
    with open(PROJECT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_projects(projects):
    with open(PROJECT_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, indent=4)

def last_id(data_list):
    if len(data_list) == 0:
        return 0
    else:
        return data_list[-1]['id']

def show_projects():
    print("\n===== Projects =====")
    projects = load_projects()
    for project in projects:
        print(f"Project ID: #{project['id']}")
        print(f"Title: {project['title']}")
        print(f"Details: {project['details']}")
        print(f"Total Target: {project['total_target']} EGP")
        print(f"Start Date: {project['start_date']}")
        print(f"End Date: {project['end_date']}")
        print(f"Creator: {project['userId']}\n")

def check_number(number):
    isValid = number.isdigit()
    if not isValid:
        print(" Invalid number format. Try another number.")
    return isValid

def valid_date(date):
    pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
    isValid = re.match(pattern, date) is not None
    if not isValid:
        print(" Invalid date format. Try another date.")
    return isValid

def check_end_date_after_start_date(start_date, end_date):
    isValid = start_date < end_date
    if not isValid:
        print(" End date must be after start date.")
    return isValid

def show_project_menu():
    print("\nPlease choose an option:")
    print("1. Show projects")
    print("2. Add project")
    print("3. Edit project")
    print("4. Delete project")
    print("0. Exit")

def project_menu():
    while True:
        show_project_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            show_projects()
        elif choice == '2':
            add_project()
        elif choice == '3':
            edit_project()
        elif choice == '4':
            delete_project()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def add_project():
    print("\n===== Add Project =====")
    projects = load_projects()

    title = ""
    while title == "":
        title = input("Title: ").strip()

    details = ""
    while details == "":
        details = input("Details: ").strip()

    total_target = ""
    while total_target == "" or not check_number(total_target):
        total_target = input("Total Target: ").strip()

    start_date = ""
    while start_date == "" or not valid_date(start_date):
        start_date = input("Start Date: ").strip()

    end_date = ""
    while end_date == "" or not valid_date(end_date) or not check_end_date_after_start_date(start_date, end_date):
        end_date = input("End Date: ").strip()

    projects.append({
        "id": last_id(projects) + 1,
        "title": title,
        "details": details,
        "total_target": int(total_target),
        "start_date": start_date,
        "end_date": end_date,
        "userId": logged_in_user
    })
    save_projects(projects)
    print("Project added successfully!")

def edit_project():
    print("\n===== Edit Project =====")
    projects = load_projects()

    project_id = ""
    while project_id == "" or not check_number(project_id):
        project_id = input("Project ID: ").strip()
    project_id = int(project_id)

    project = next((project for project in projects if project['id'] == project_id), None)
    if project is None:
        print("Project not found.")
    elif project['userId'] != logged_in_user:
        print("You are not the creator of this project.")
    else:
        title = input(f"Title ({project['title']}): ").strip() or project['title']
        details = input(f"Details ({project['details']}): ").strip() or project['details']

        # Total Target
        while True:
            total_target = input(f"Total Target ({project['total_target']}): ").strip()
            if total_target == "":
                total_target = project['total_target']
                break
            elif check_number(total_target):
                break

        # Start Date
        while True:
            start_date = input(f"Start Date ({project['start_date']}): ").strip()
            if start_date == "":
                start_date = project['start_date']
                break
            elif valid_date(start_date):
                break

        # End Date
        while True:
            end_date = input(f"End Date ({project['end_date']}): ").strip()
            if end_date == "":
                end_date = project['end_date']
                break
            elif valid_date(end_date) and check_end_date_after_start_date(start_date, end_date):
                break

        project['title'] = title
        project['details'] = details
        project['total_target'] = int(total_target)
        project['start_date'] = start_date
        project['end_date'] = end_date

        save_projects(projects)
        print("Project edited successfully!")

def delete_project():
    print("\n===== Delete Project =====")
    projects = load_projects()

    project_id = ""
    while project_id == "" or not check_number(project_id):
        project_id = input("Project ID: ").strip()
    project_id = int(project_id)

    project = next((project for project in projects if project['id'] == project_id), None)
    if project is None:
        print("Project not found.")
    elif project['userId'] != logged_in_user:
        print("You are not the creator of this project.")
    else:
        projects.remove(project)
        save_projects(projects)
        print("✅ Project deleted successfully!")

# AUTHENTICATION
#############################
def load_users():
    with open(USER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_egyptian_phone(phone):
    isValid = re.fullmatch(r'01[0125][0-9]{8}', phone) is not None
    if not isValid:
        print("Invalid Egyptian phone number. Must match pattern 01[0,1,2,5] + 8 digits.")
    return isValid

def email_exists(email, users):
    isExists = any(user['email'].lower() == email.lower() for user in users)
    if isExists:
        print("Email already exists. Try another email.")
    return isExists

def is_valid_email(email):
    isValid = re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) is not None
    if not isValid:
        print("Invalid email format. Try another one.")
    return isValid

def password_check(password):
    isValid = len(password) >= 3
    if not isValid:
        print("Password must be at least 3 characters long.")
    return isValid

def check_confirm_password(password, confirm_password):
    isValid = password == confirm_password
    if not isValid:
        print("Passwords do not match.")
    return isValid

def login():
    print("\n===== Login =====")
    global logged_in_user
    users = load_users()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    hashed = hash_password(password)

    for user in users:
        if user['email'].lower() == email.lower() and user['password'] == hashed:
            print(f"Welcome back, {user['first_name']} {user['last_name']}!")
            logged_in_user = user['email']
            project_menu()
            return
    print("Invalid email or password.")

def register():
    print("\n===== Register =====")
    users = load_users()

    first_name = ""
    while first_name == "":
        first_name = input("First name: ").strip()

    last_name = ""
    while last_name == "":
        last_name = input("Last name: ").strip()

    email = ""
    while email == "" or email_exists(email, users) or not is_valid_email(email):
        email = input("Email: ").strip()

    password = ""
    while password == "" or not password_check(password):
        password = input("Password: ").strip()

    confirm_password = ""
    while confirm_password == "" or not check_confirm_password(password, confirm_password):
        confirm_password = input("Confirm password: ").strip()

    mobile = ""
    while mobile == "" or not is_valid_egyptian_phone(mobile):
        mobile = input("Mobile phone: ").strip()

    users.append({
        "first_name": first_name,
        "last_name": last_name,
        "email": email.lower(),
        "password": hash_password(password),
        "mobile": mobile
    })
    save_users(users)
    print("Registered successfully!")
# MAIN MENU 
##############################
def show_menu():
    print("\nPlease choose an option:")
    print("1. Login")
    print("2. Register")
    print("0. Exit")

def main_menu():
    print("===== Crowd-Funding console app =====")
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            login()
        elif choice == '2':
            register()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# MAIN
##############################
if __name__ == "__main__":
    for file in [USER_FILE, PROJECT_FILE]:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)

    main_menu()