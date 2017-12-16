#!/usr/bin/python
# A Command Line Based TODO Manager

import sys
import os
from subprocess import call
import json
import argparse
from pprint import pprint

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

def todo_add():
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

def save_tasks(todos_list = None):
    tasks = []
    pending_tasks = [p_task for p_task in todos_list if p_task['STATUS'] == 'TODO']
    done_tasks = [d_task for d_task in todos_list if d_task['STATUS'] == 'DONE']
    pending_tasks = sorted(pending_tasks, key=lambda k: k['PRIORITY'])
    done_tasks = sorted(done_tasks, key=lambda k: k['PRIORITY'])
    tasks.extend(pending_tasks)
    tasks.extend(done_tasks)
    with open(source_file, 'w') as fp:
        json.dump(tasks, fp)


def todo_del():
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

def todo_status(action, prev_state = None, new_state = None):
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
    if len(todos) == 0:
         sys.stdout.write("\n" + bcolors.WARNING + "You have NO tasks!\n\n" + bcolors.ENDC)
         exit()
    if not custom_list:
        custom_list = todos
    for i in range(len(custom_list)):
        todo_print(custom_list[i], i)
    sys.stdout.write("\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("action", type=str,
                        help="Available options: add, del, mark, unmark, list, help" )
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
    if args.action == 'source':
        sys.stdout.write("\n Source: /tmp/.todo.json\n")

