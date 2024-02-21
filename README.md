## Description ⚓
The AirBnB project is simple copy of AirBnB website . we will not  implement all the features, only some
all fundamental concepts of the higher level programming track.

The project currently implement stoage abstraction usin MySQL

## Concepts to Learn ⏰
 - What is Unit testing and how to implement it in a large project
 - What is *args and how to use it
 - What is **kwargs and how to use it
 - How to handle named arguments in a function
 - How to create a MySQL database
 - How to create a MySQL user and grant it privileges
 - What ORM means
 - How to map a Python Class to a MySQL table
 - How to handle 2 different storage engines with the same codebase
 - How to use environment variables
## Console 💻
the console is command line interpreter that permits management of Backend of AirBnB project. 
 - create teh data model
 - manage (create, update, destroy, etc) objects via a console / command interpreter
 - store and persist objects to a file (JSON file)
### Using the Console
The AirBnB console can be run both interactively and non-interactively. 
To run the console in non-interactive mode, pipe any command(s) into an execution 
of the file `console.py` at the command line.

``
$ ./console.py
(hbnb) help
Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb) 
(hbnb) 
(hbnb) quit
$
```
also in non-interactive mode
```
$ echo "help" | ./console.py
(hbnb)
Documented commands (type help <topic>):
EOF  help  quit
(hbnb)
$
$ cat test_help
help
$
$ cat test_help | ./console.py
(hbnb)
Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
$
``
## Authors
* **Kaoutar En-Nabirha** <[KAWTREN]>
* **Ouafae Saim**  <[ouafcode]>
