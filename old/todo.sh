#!/bin/sh
DATABASE=todo.db
SQL=create.sql

# If database file exists
if [ -f $DATABASE ]; then
	# If more than 0 arguments were supplied
	if [ $# -gt 0 ]; then
		# If user wants to reset ToDo Database
		if [ $1 == "-n" ] || [ $1 == "--new" ]; then
			# Run create.sql on Database and open ToDo Shell
			sqlite3 $DATABASE < $SQL
			python main.py $DATABASE "-s"
		else
			# Otherwise pass arguments to program
			python main.py $DATABASE $1 $2 $3
		fi
	else
		# Display the ToDo Task-List
		python main.py $DATABASE
	fi
else
	# Create Database File and start ToDo List shell
	touch $DATABASE
	sqlite3 $DATABASE < $SQL
	python main.py $DATABASE "-s"
fi