To-Do-List Command Line Utility
===============================

Simple Command Line Utility that works as a To-Do-List using an SQLite3 database.

The to-do-list consists of a task list made up of individual tasks. 
Each task has a name and a status. 
The status can be in three states: 

- o or 0 for "no progress"
- - or 1 for "in progress"
- x or 2 for "completed"
 
The to-do-list is accessed with the command todo, and can either be used in "shell mode" which is essentially a shell where you can manipulate your todo list, or in command-line mode where you simply supply arguments to the todo command without needing to enter the shell.
The current create SQL contains a schema for tag support, and that is currently my next goal. I would also like to add support for formatted dates and more complex shell features.
