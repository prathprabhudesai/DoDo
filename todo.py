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

def todo_mark():
    """
    Function to change status of a task to marked state.
    """
    display_tasks = [x_task for x_task in todos if x_task['STATUS']=='TODO']
    if len(display_tasks) == 0:
        print "No tasks to mark"
        exit()

    counter, value = [], []
    for c, v in enumerate(display_tasks,1):
        print c, v
        counter.append(c)
        value.append(v)

    try:
        mark_opt = int(raw_input("Select option to be marked \n ->"))
        if mark_opt not in range(1,len(display_tasks)+1):
            print "Invalid option"
            exit()
    except ValueError as error:
        print "Please entire valid number"
        exit()

    mark_task = [task['NAME'] for cnt, task in zip(counter, value) if cnt == mark_opt]
    for x_task in todos:
       if mark_task[0] == x_task['NAME']:
           x_task['STATUS'] = "DONE"
           with open(source_file, 'w') as fp:
               json.dump(todos, fp)
           print "Task %s successfully marked"%(str(mark_task[0]))
           break



def todo_unmark():
    print "Mark as done as not done -> so TODO"


def todo_print(todo):
    if todo['STATUS'] == "TODO":
        sys.stdout.write(" " + bcolors.FAIL + " ( TODO ) " + todo['PRIORITY'] +
                         " " + bcolors.ENDC + todo['NAME'])
        if len(todo['DESC'].lstrip().rstrip()) > 0:
            sys.stdout.write(" (" + todo['DESC'].lstrip().rstrip() + ")")
        if len(todo['DEADLINE'].lstrip().rstrip()) > 0:
            sys.stdout.write(bcolors.OKBLUE + " :" + todo['DEADLINE'].lstrip().rstrip() + ":"
                             + bcolors.ENDC)
    elif todo['STATUS'] == "DONE":
        sys.stdout.write(" " + bcolors.OKGREEN + "( DONE ) " +
                         bcolors.ENDC + todo['NAME'])
        if len(todo['DESC'].lstrip().rstrip()) > 0:
            sys.stdout.write(
                " (" + todo['DESC'].lstrip().rstrip() + ")")
    print ""
            
def todo_list():
    if len(todos) == 0:
        print "NO TASKS"
    for i in range(len(todos)):
        todo_print(todos[i])

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
        todo_mark()
    if args.action == 'unmark':
        todo_unmark()
    if args.action == 'list':
        todo_list()
    if args.action == 'help':
        todo_usage()
