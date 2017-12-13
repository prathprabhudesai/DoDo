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
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def todo_add():
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
    with open(source_file, 'w') as fp:
        json.dump(todos, fp)

def todo_del():
    print "Delete from the list"

def todo_status(prev_state = None, new_state = None):
    """
    Function to change status of a task to marked state.
    :param prev_state: State before changing state of a task
    :param new_state: Updated state of a task
    """

    display_tasks = [x_task for x_task in todos if x_task['STATUS'] == prev_state]
    if len(display_tasks) == 0:
        print "No tasks to mark/unmark"
        exit()

    counter, value = [], []
    print display_tasks
    todo_list(custom_list=display_tasks)

    try:
        mark_opt = int(raw_input("Select task number \n ->"))
        if mark_opt not in range(len(display_tasks)):
            print "Invalid option"
            exit()
    except ValueError as error:
        print "Please entire valid number"
        exit()

    mark_task = [task['NAME'] for cnt, task in enumerate(display_tasks) if cnt == mark_opt]
    for x_task in todos:
       if mark_task[0] == x_task['NAME']:
           x_task['STATUS'] = new_state
           with open(source_file, 'w') as fp:
               json.dump(todos, fp)
           print "Task %s successfully updated"%(str(mark_task[0]))
           break



def todo_print(todo, i):

    if todo['STATUS'] == "TODO":
        sys.stdout.write(str(i)+ " " + bcolors.FAIL + " ( TODO ) " + todo['PRIORITY'] +
                         " " + bcolors.ENDC + todo['NAME'])
        if len(todo['DESC'].lstrip().rstrip()) > 0:
            sys.stdout.write(" (" + todo['DESC'].lstrip().rstrip() + ")")
        if len(todo['DEADLINE'].lstrip().rstrip()) > 0:
            sys.stdout.write(bcolors.OKBLUE + " :" + todo['DEADLINE'].lstrip().rstrip() + ":"
                             + bcolors.ENDC)
    elif todo['STATUS'] == "DONE":
        sys.stdout.write(str(i) + " " + bcolors.OKGREEN + "( DONE ) " +
                         bcolors.ENDC + todo['NAME'])
        if len(todo['DESC'].lstrip().rstrip()) > 0:
            sys.stdout.write(
                " (" + todo['DESC'].lstrip().rstrip() + ")")
    print ""

def todo_list(custom_list=None):
    if len(todos) == 0:
        print "NO TASKS"
    if not custom_list:
        custom_list = todos
    for i in range(len(custom_list)):
        todo_print(custom_list[i], i)

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
        todo_status(prev_state = 'TODO', new_state = 'DONE')
    if args.action == 'unmark':
        todo_status(prev_state = 'DONE', new_state = 'TODO')
    if args.action == 'list':
        todo_list()
    if args.action == 'help':
        todo_usage()
