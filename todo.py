#!/usr/bin/python
# A Command Line Based TODO Manager

import sys
import os
from subprocess import call
import json
import argparse
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


# source file
source_file = "/tmp/.todo.json"

# global dictionary to maintain list of tasks
todos = json.load(open(source_file))

# color coding for the list output
class bcolors:
    HEADER = '\033[95m'
    DEADLINE = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def save_tasks(todos_list = None):
    '''
    :param todos_list: the list of all the tasks
    :return:
    '''
    tasks = []
    pending_tasks = [p_task for p_task in todos_list if p_task['STATUS'] == 'TODO']
    done_tasks = [d_task for d_task in todos_list if d_task['STATUS'] == 'DONE']
    pending_tasks = sorted(pending_tasks, key=lambda k: k['PRIORITY'])
    done_tasks = sorted(done_tasks, key=lambda k: k['PRIORITY'])
    tasks.extend(pending_tasks)
    tasks.extend(done_tasks)
    with open(source_file, 'w') as fp:
        json.dump(tasks, fp)
    
def todo_add():
    '''
    :return: void
    '''
    sys.stdout.write("\n")
    what = str(raw_input("What? : "))
    description = str(raw_input("Description: "))
    deadline = str(raw_input("When? : "))
    priority = str(raw_input("Priority ([A]/B/C): "))
    if priority == "":
        priority = "A"
    task = {}
    task['NAME'] = what
    task['STATUS'] = "TODO"
    task['DESC'] = description
    task['DEADLINE'] = deadline
    task['PRIORITY'] = "[#" + priority.upper() + "]"
    todos.append(task)
    save_tasks(todos)
    sys.stdout.write("" + bcolors.WARNING + "Task Added! \n" + bcolors.ENDC)

def todo_del():
    '''
    :return: void
    '''
    todo_list()
    try:
        del_opt = int(raw_input("Which one? : "))
        del_opt = del_opt - 1
        if del_opt not in range(len(todos)):
            sys.stdout.write("" + bcolors.FAIL + "This task number is not there :-(\n")
            exit()
    except ValueError as error:
        exit()
    del_task = [task['NAME'] for cnt, task in enumerate(todos) if cnt == del_opt]
    for task in todos:
        if task['NAME'] == del_task[0]:
            break
    todos.remove(task)
    save_tasks(todos)
    sys.stdout.write("" + bcolors.WARNING + "Succcessfully deleted the task :-)\n" + bcolors.ENDC)

def todo_update():
    '''
    :return: void
    '''
    todo_list()
    try:
        update_opt = int(raw_input("Which one? : "))
        update_opt = update_opt - 1
        if update_opt not in range(len(todos)):
            sys.stdout.write("" + bcolors.FAIL + "This task number is not there :-(\n")
            exit()
    except ValueError as error:
        exit()
    update_task = [task['NAME'] for cnt, task in enumerate(todos) if cnt == update_opt]
    for task in todos:
        if task['NAME'] == update_task[0]:
            sys.stdout.write("\n" + bcolors.WARNING + "1. Name\n2. Deadline\n3. Description\n4. Status\n" + bcolors.ENDC)
            option = int(raw_input("What do you want to change? : "))
            if option not in [1,2,3,4]:
                sys.stdout.write("" + bcolors.FAIL + "There's no option like that!" + bcolors.ENDC)
                exit()
            if option == 1:
                new_name = raw_input("New Name? : ")
                task['NAME'] = new_name
            elif option == 2:
                new_deadline = raw_input("New Deadline? : ")
                task['DEADLINE'] = new_deadline
            elif option == 3:
                new_desc = raw_input("New Description? : ")
                task['DESC'] = new_desc
            elif option == 4:
                new_status = raw_input("New Status? mark/unmark : ")
                if new_status.upper() == "MARK": 
                    task['STATUS'] = "DONE"
                elif new_status.upper() == "UNMARK":
                    task['STATUS'] = "TODO"
            else:
                exit()
            save_tasks(todos)
            sys.stdout.write("" + bcolors.WARNING + "Successfully updated the task :-)\n" + bcolors.ENDC)
            break
        
def todo_status(action, prev_state = None, new_state = None):
    '''
    :param action: it is the input action mark or unmark
    :param prev_state: the previosu state of the task
    :param new_state: new state of the task
    :return: void
    '''
    display_tasks = [x_task for x_task in todos if x_task['STATUS'] == prev_state]
    if len(display_tasks) == 0:
        sys.stdout.write("" + bcolors.FAIL + "NO TASKS to " + bcolors.FAIL + action + "\n" + bcolors.ENDC)
        exit()
    todo_list(custom_list=display_tasks)
    try:
        mark_opt = int(raw_input("Which one? : "))
        mark_opt = mark_opt - 1
        if mark_opt not in range(len(display_tasks)):
            sys.stdout.write("" + bcolors.FAIL + "This task number is not there :-(\n")
            exit()
    except ValueError as error:
        sys.stdout.write("" + bcolors.FAIL + "This task number is not there :-(\n" + bcolors.ENDC)
        exit()
    mark_task = [task['NAME'] for cnt, task in enumerate(display_tasks) if cnt == mark_opt]
    for x_task in todos:
       if mark_task[0] == x_task['NAME']:
           x_task['STATUS'] = new_state
           save_tasks(todos)
           sys.stdout.write("" + bcolors.WARNING + "Successfully updated the task :-)\n" + bcolors.ENDC)
           break

def todo_print(todo, i):
    '''
    :param todo: task
    :param i: index
    :return: void
    '''
    sys.stdout.write("\n")
    if todo['STATUS'] == "TODO":
        sys.stdout.write(str(i+1)+ " " + bcolors.FAIL + "( TODO ) " + todo['PRIORITY'] +
                         " " + bcolors.ENDC + todo['NAME'])
        if len(todo['DESC'].lstrip().rstrip()) > 0:
            sys.stdout.write(" (" + todo['DESC'].lstrip().rstrip() + ")")
        if len(todo['DEADLINE'].lstrip().rstrip()) > 0:
            sys.stdout.write(bcolors.DEADLINE + " :" + todo['DEADLINE'].lstrip().rstrip() + ":"
                             + bcolors.ENDC)
    elif todo['STATUS'] == "DONE":
        sys.stdout.write(str(i+1) + " " + bcolors.SUCCESS + "( DONE ) " +
                         bcolors.ENDC + todo['NAME'])
        if len(todo['DESC'].lstrip().rstrip()) > 0:
            sys.stdout.write(
                " (" + todo['DESC'].lstrip().rstrip() + ")")
    sys.stdout.write("\n")

def todo_list(custom_list=None):
    '''
    :param custom_list: custom / filtered list of tasks
    :return: void
    '''
    if len(todos) == 0:
         sys.stdout.write("\n" + bcolors.WARNING + "You have NO tasks!\n\n" + bcolors.ENDC)
         exit()
    if not custom_list:
        custom_list = todos
    for i in range(len(custom_list)):
        todo_print(custom_list[i], i)
    sys.stdout.write("\n")

def todo_notify(status='ALL'):
    '''
    :param status: Tasks to be notified over email based on status
    :return: void
    '''
    fromaddr = "mrunmayeejog.i@gmail.com"
    toaddr = "mrunmayeejog.i@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "DoDo Tasks"

    tasks = todos
    body = []
    if status == 'ALL':
        body.append(todos)
      
    if status == 'TODO':
        for i in range(len(tasks)):
            if todos[i]['STATUS'] == "TODO":
                body.append(todos[i])
    if status == 'DONE':
        for i in range(len(tasks)):
            if todos[i]['STATUS'] == "DONE":
                body.append(todos[i])

    msg.attach(MIMEText("Hello !!\n\n" + str(body) + "\n\nHave a great day !!", 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "mrunmayee11")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("action", type=str,
                        help="Available options: add, del, mark, unmark, list, update, help" )
    args = parser.parse_args()
    if args.action == 'add':
        todo_add()
    if args.action == 'del':
        todo_del()
    if args.action == 'mark':
        todo_status('MARK', prev_state = 'TODO', new_state = 'DONE')
    if args.action == 'unmark':
        todo_status('UNMARK', prev_state = 'DONE', new_state = 'TODO')
    if args.action == 'list':
        todo_list()
    if args.action == 'help':
        todo_usage()
    if args.action == 'update':
        todo_update()
    if args.action == 'source':
        sys.stdout.write("\n Source: /tmp/.todo.json\n")
    if args.action == 'notify':
        todo_notify(status = 'ALL')
