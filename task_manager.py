import os
from datetime import date, datetime

#changed "%d-%m-%Y" to "%d %b %Y" to accurately match the date format in task.txt
DATETIME_STRING_FORMAT = "%d %b %Y"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None, number = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed
        self.number = number

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        #Changed argument ";" to ", " in order to split data in tasks.txt
        tasks = task_str.split(", ")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        number = tasks[6]
        self.__init__(username, title, description, due_date, assigned_date, completed, number)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No",
            self.number
        ]
        #Changed to separator from ";" to ", "
        return ", ".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        #Display completion status
        disp_str += f"Task Complete? \t {self.completed}\n"
        disp_str += f"Task Number: \t {self.number}\n"
        disp_str += f"Task Description: \n{self.description}\n"
        return disp_str
        


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)  

# Read and parse user.txt
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin, password") 

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    #Changed argument ";" to ", " to in order to split data in user.txt
    username, password = user.split(", ")
    username_password[username] = password

# Keep trying until a successful login
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

def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    #Changed ";" to ", " in all instances that occured in "validates_string" and "check_username_and_password" as this is the new separator in the data
    if ", " in input_str:
        print("Your input cannot contain a ', ' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ', ' character cannot be in the username or password
    if ", " in username or ", " in password:
        print("Username or password cannot contain ', '.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
        #Changed (f"{k};{username_dict[k]} to f"{k}, {username_dict[k]}) so the username, password data for future users can be split, as I changed the argument for split to ", "
            user_data.append(f"{k}, {username_dict[k]}")
        out_file.write("\n".join(user_data))

def reg_user():
    while True:
        #Check if "curr_user" is "admin", if not then print message and break out of while loop
        if curr_user != 'admin':
            print("Registering new users requires admin privileges")
            break
        new_username = input("New Username: ")
        
        #If username is duplicate, print error and break
        if new_username in username_password.keys():
            print("User already exists. Please enter a new user")
            break

        # Request input of a new password
        new_password = input("New Password: ")

        if not check_username_and_password(new_username, new_password):
            # Username or password is not safe for storage - continue
            break

        # Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If they are the same, add them to the user.txt file,
            print("New user added")

            # Add to dictionary and write to file
            username_password[new_username] = new_password
            write_usernames_to_file(username_password)
            break

        # Otherwise you present a relevant message.
        else:
            print("Passwords do no match")

def add_task():
    while True:
    # Ask for username
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            break

        # Get title of task and ensure safe for storage
        while True:
            task_title = input("Title of Task: ")
            if validate_string(task_title):
                break

        # Get description of task and ensure safe for storage
        while True:
            task_description = input("Description of Task: ")
            if validate_string(task_description):
                break

        # Obtain and parse due date
        while True:
            try:
            #changed date abbreviation to "DD Mmm YYYY" to match "DATETIME_STRING_FORMAT"
                task_due_date = input("Due date of task (DD Mmm YYYY): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Obtain and parse current date
        curr_date = date.today()

        #Obtain task number of user
        task_number_count = 0
        for x in task_list:
            if x.username == task_username:
                task_number_count +=1
        task_number = task_number_count + 1
        task_number = str(task_number)
        
        # Create a new Task object and append to list of tasks
        new_task = Task(task_username, task_title, task_description, due_date_time,curr_date, False, task_number)
        task_list.append(new_task)

        # Write to tasks.txt
        with open("tasks.txt", "w") as task_file:
            task_file.write("\n".join([t.to_string() for t in task_list]))
        print("Task successfully added.")
        break

def view_all():
    print("-----------------------------------")
#Check if there are any tasks, if not print "There are no tasks."
    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

#print each task in task_list using "display()" function
    for t in task_list:
        print(t.display())
        print("-----------------------------------")

def view_mine():
    #checkpoint 1
    checkpoint1 = 1
    while checkpoint1 == 1:

        #Print tasks that belong to the "curr_user"
        print("-----------------------------------")
        has_task = False
        for t in task_list:
            if t.username == curr_user:
                has_task = True
                print(t.display())
                print("-----------------------------------")
    

        #Ask user to select task by entering task number, if "-1 entered go to menu"
        task_number = int(input("Choose task number, enter -1 to return to menu: "))
        #"max_number" variable counts how many tasks the current user has
        max_number = 0
        for x in task_list:
            if x.username == curr_user:
                max_number += 1
        #Go back to menu if "task_number" is -1      
        if task_number == -1:
            checkpoint1 = 0
        #If chosen "task_number" > than total number of tasks that user has, print error message and return to menu
        elif task_number > max_number or task_number == 0:
            print("Error, no task found.")
            checkpoint1 = 0


        #If "task_number" is a suitable number, then enter checkpoint 2
        else:  
            checkpoint2 = 1
            while checkpoint2 == 1:
                #Ask user if they want to edit or mark the task
                mark_or_edit = input("Would you like to mark the task as complete or edit the task? Mark/edit: ")


                #If user wants to mark, ask user to input completion status
                if mark_or_edit.lower() == "mark":
                    completion = input("Is task completed? ")
                    #If completion status is "yes", iterate through "task_list" and find matching task (same username and task number). Change that task's.completed to True
                    if completion.lower() == "yes":
                        for a in task_list:
                            if a.username == curr_user and a.number == str(task_number):                            
                                a.completed = True
                                #Go back to menu after marking task as complete
                                checkpoint2, checkpoint1 = 0, 0
                    #If user enters anything but "yes" go back to menu and print message            
                    else:
                        print("Come back when task is complete.")
                        checkpoint2, checkpoint1 = 0, 0


                #If user wants to edit, enter checkpoint 3
                elif mark_or_edit.lower() == "edit":
                    checkpoint3 = 1
                    while checkpoint3 == 1:
                        #Iterate through "task_list" to check if the chosen task is completed or not
                        for b in task_list:
                            #If task not completed, user enters the "new_username"
                            if b.username == curr_user and b.number == str(task_number) and b.completed == False:
                                new_username = input("Enter the new user of this task: ")
                                #If username doesn't exist, print error message and go back to checkpoint 3
                                if new_username not in username_password.keys():
                                    print("User does not exist. Please enter a valid username")


                                #If username exists, change this this tasks username to inputted username
                                else:
                                    b.username = new_username
                                    #Count the number of tasks the new user has already
                                    task_count = 0
                                    for z in task_list:
                                        if z.username == new_username:
                                            task_count +=1
                                    #Make this task's number the amount of tasks the user has + 1
                                    b.number = str(task_count)                            
                                    
                                    
                                    #Obtain and parse due date
                                    while True:
                                        try:    
                                            task_due_date = input("New due date of task (DD Mmm YYYY): ")
                                            b.due_date = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                                            break
                                        except ValueError:
                                            print("Invalid datetime format. Please use the format specified")
                                    

                                    #Make sure the current user logged in user and the new user receiving the task has task numbers that make sense
                                    curr_user_count = 0
                                    new_user_count = 0                                 
                                    for x in task_list:
                                        #Iterate through "task_list". Increment "curr_user_count" by 1 each time current user has a task, change that task's number to "curr_user_count"
                                        if x.username == curr_user:
                                            curr_user_count += 1
                                            x.number = str(curr_user_count)
                                        #Do the same for the new user the task was assigned to
                                        elif x.username == new_username:
                                            new_user_count += 1
                                            x.number = str(new_user_count)
                                    #Go back to menu after editing task
                                    checkpoint3, checkpoint2, checkpoint1 = 0, 0, 0


                            #If the task user tried to edit is already complete, print error message and go back to menu 
                            elif b.username == curr_user and b.number == str(task_number) and b.completed == True:
                                print("Cannot edit a complete task.")
                                checkpoint3, checkpoint2, checkpoint1 = 0, 0, 0


                #If user didn't chose mark or edit, print message and return to checkpoint 2
                else:
                    print("Please choose mark or edit.")


    #Write to tasks.txt, note this is outside of checkpoin 1 while loop, so updated tasks are written to "tasks.txt" every time user does something with view my task ("vm")    
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))

def generate_reports():
    #Obtain total number of tasks and create variables to keep count of occurences
    total = len(task_list)
    completed_counter = 0
    incomplete_counter = 0
    overdue_counter = 0
    #Obtain today's date - use datetime to match date format in the task Class
    today_date = datetime.today()

    #Iterate through "task_list" and increment respective counters if task is completed, incomplete, or overdue
    for x in task_list:
        if x.completed == True:
            completed_counter += 1
        if x.completed == False:
            incomplete_counter += 1
        if x.due_date < today_date and x.completed == False:
            overdue_counter += 1

    #Calculate percentages of uncompleted and overdue tasks
    percentage_incomplete = round((incomplete_counter/total)*100,)
    percentage_overdue = round((overdue_counter/total)*100,)

    #Create a list of all the information required for "task_overview.txt" 
    tsk_ovw_list = [
    f"Total number of tasks: {total}", 
    f"Completed tasks: {completed_counter}", 
    f"Uncompleted tasks: {incomplete_counter}",
    f"Overdue tasks: {overdue_counter}",
    f"Percentage of uncompleted tasks: {percentage_incomplete}%",
    f"Percentage of overdue tasks: {percentage_overdue}%"
    ]

    #Write each element into "task_overview.txt", each in a new line, in a readable manner
    with open("task_overview.txt","w") as f:
        for x in tsk_ovw_list:
            f.write(x + "\n")

    #Open file "user_overview.txt" 
    with open ("user_overview.txt","w") as user_file:
        #Obtain total number of users from dictionary "username_password"
        num_users = len(username_password.keys())
        #Write total number of users and total number of tasks 
        user_file.write(f"Total number of users: {num_users}\nTotal number of tasks: {total}\n\n")

        #Use for loop to iterate through usernames (using the keys of dictionary "username_password")
        for u in username_password.keys():
            #Start by writing username and display user-specific information below
            user_file.write(f"{u}:")
            #Create counters to increment user-specific information using another for loop below
            user_task_num = 0
            user_comp_tsk = 0
            user_incomp_tsk = 0
            user_overdue_tsk = 0

            #For loop to iterate through "task_list" for each user. Increment counter for every task, completed task, uncompleted task, and overdue task
            for task in task_list:
                if task.username == u:
                    user_task_num += 1
                if task.username == u and task.completed == True:
                    user_comp_tsk += 1
                if task.username == u and task.completed == False:
                    user_incomp_tsk += 1
                if task.username == u and task.due_date < today_date and task.completed == False:
                    user_overdue_tsk += 1

            #If user has no tasks, assign 0 to all statistics
            if user_task_num == 0:
                per_tasks, per_comp_tasks, per_incomp_tasks, per_overdue_tasks = 0, 0, 0, 0
            else:
            #Calculate percentages used to display in "user_overview.txt"        
                per_tasks = round((user_task_num/total) * 100,)
                per_comp_tasks = round((user_comp_tsk/user_task_num) * 100,)
                per_incomp_tasks = round((user_incomp_tsk/user_task_num) * 100,)
                per_overdue_tasks = round((user_overdue_tsk/user_task_num) * 100,)

            #Write required information in readable manner into "user_overview.txt"
            user_file.write(f"""
Number of tasks: {user_task_num}
Percentage of tasks: {per_tasks}%
Percentage of completed tasks: {per_comp_tasks}%
Percentage of uncompleted tasks: {per_incomp_tasks}%
Percentage of overdue tasks: {per_overdue_tasks}%\n\n""")
                
    #Print message to user saying reports have been generated, use function display_statistics() (defined below) to view
    print("Reports generated, input 'ds' to view.")

def display_statistics():
    #If "task_overview.txt" or "user_overview.txt" don't exist, call generate_reports() 
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    #Create empty string variable to store contents from both "task_overview.txt" and "user_overview.txt" 
    contents_tsk_ovw = ""
    with open("task_overview.txt", "r") as tsk_ovw_file:
        for line in tsk_ovw_file:
            contents_tsk_ovw += line
    contents_user_ovw = ""
    with open("user_overview.txt", "r") as user_ovw_file:
        for line in user_ovw_file:
            contents_user_ovw += line

    #Print information to output in a readable and user-friendly manner
    print("-----------------------------------")
    print("TASK OVERVIEW:")
    print(contents_tsk_ovw)
    print("-----------------------------------")
    print("USER OVERVIEW")
    print(contents_user_ovw)
    print("-----------------------------------")
    
#########################
# Main Program
######################### 

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
    : ''').lower()

    if menu == 'r': # Register new user (if admin)
        # Request input of a new username
        reg_user()
        
    elif menu == 'a': # Add a new task
        add_task()

    elif menu == 'va': # View all tasks
        view_all()

    elif menu == 'vm': # View my tasks
        view_mine()
    
    elif menu == 'gr' and curr_user == 'admin': # If admin, generate reports
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin': # If admin, display statistics
        display_statistics()

    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else: # Default case
        print("You have made a wrong choice, Please Try again") 