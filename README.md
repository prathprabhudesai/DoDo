# DoDo
A simple CLI based todo app

## Installation
1. Fork this repository and clone it: <code>git clone https://github.com/prathprabhudesai/DoDo.git</code>
2. Go to the cloned folder and run the setup script: <code>./setup.sh</code>

## Usage
DoDo currently supports basic functionality such as adding tasks, clearing, marking them as done or undone, assigning priority etc.

####$ todo add
````
What? : Appointment
Description: Dental Checkup at Dr. Harris's Clinic
When? : Tomorrow 9 pm
Priority ([A]/B/C): A
Task Added!
````
####$ todo list
````
1 ( TODO ) [#A] Appointment (Dental Checkup at Dr. Harris's Clinic) :Tomorrow 9 pm:
````
####$ todo mark
````
1 ( TODO ) [#A] Appointment (Dental Checkup at Dr. Harris's Clinic) :Tomorrow 9 pm:

Which one? : 1
Successfully updated the task :-)
````

