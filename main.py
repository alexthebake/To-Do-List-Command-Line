# ToDo List App
# -- SQLite Version
import sys
import sqlite3 as db
from time import time
from os.path import isfile

class SQlite3_Task(object):
	def __init__(self, item):
		self.id = item[0]
		self.created = item[1]
		self.status = item[2]
		self.name = item[3]
		self.status_map = {
			0 : 'o',
			1 : '-',
			2 : 'x'
		}
		self.format_status = self.status_map[self.status]

	def update(self, status):
		self.status = int(status)
		self.format_status = self.status_map[self.status]

	def rename(self, name):
		self.name = name

	def show(self, spaces=''):
		return str(self.id) + spaces + ' | ' + self.format_status + ' | ' + self.name

class SQlite3_TaskList(object):
	def __init__(self, database_name):
		self.database_name = database_name
		self.table_name = 'Tasks'
		self.conn = self.connect()
		self.cursor = self.conn.cursor()
		self.task_list = self.get_data()
		self.n_tasks = len(self.task_list)

	def connect(self):
		if isfile(self.database_name):
			return db.connect(self.database_name)
		else:
			print 'Database not found...'
			sys.exit()

	def get_data(self):
		sql = 'SELECT * FROM ' + self.table_name
		self.cursor.execute(sql)
		return {item[0] : SQlite3_Task(item) for item in self.cursor.fetchall()}

	def checkTaskId(self, task_id):
		return True if task_id not in self.task_list else False

	def checkStatus(self, status):
		return True if int(status) not in [0,1,2] else False

	def getStatus(self, status):
		if type(status) is str:
			if status in ['o','-','x']:
				return {'o':'0','-':'1','x':'2'}[status]
			elif int(status) in [0,1,2]:
				return status
		elif type(status) is int and status in [0,1,2]:
			return str(status)
	
	def addTask(self, name):
		created = str(time())
		sql = "INSERT INTO " + self.table_name + " (name, created) VALUES (?,?)"
		self.cursor.execute(sql, (name, created))
		self.conn.commit()

		# Use created time stamp as a unique id for new task
		sql = 'SELECT * FROM ' + self.table_name + ' WHERE created=' + created
		self.cursor.execute(sql)
		item = self.cursor.fetchone()
		self.task_list[item[0]] = SQlite3_Task(item)
		self.n_tasks += 1

	def updateTask(self, task_id, status):
		status = self.getStatus(status)
		if self.checkTaskId(task_id):
			print 'Task', str(task_id), 'not found...'
			return
		if self.checkStatus(status):
			print 'Not a valid status...'
			return
		
		sql = 'UPDATE ' + self.table_name + ' SET status=? WHERE task_id=?'
		self.cursor.execute(sql, (status, str(task_id)))
		self.conn.commit()
		
		self.task_list[task_id].update(status)

	def removeTask(self, task_id):
		if task_id not in self.task_list:
			print 'Task not found...'
			return
		sql = 'DELETE FROM ' + self.table_name + ' WHERE task_id=' + str(task_id)
		self.cursor.execute(sql)
		self.conn.commit()
		
		del self.task_list[task_id]
		self.n_tasks -= 1

	def renameTask(self, task_id, name):
		if self.checkTaskId(task_id):
			print 'Task ' + str(task_id) + ' not found...'
			return
		sql = 'UPDATE ' + self.table_name + ' SET name=? WHERE task_id=?'
		self.cursor.execute(sql, (name, str(task_id)))
		self.conn.commit()
		
		self.task_list[task_id].rename(name)

	def clearCompletedTasks(self):
		to_clear = [task.id for task in self.task_list.itervalues() if task.status == 2]
		for task_id in to_clear:
			self.removeTask(task_id)

	def show(self):
		print '\n========= To-Do-List ========='
		sorted_tasks = sorted(self.task_list.itervalues(), key=lambda task: task.created)
		if len(self.task_list):
			max_digits = max(len(str(k)) for k in self.task_list.iterkeys())
			for task in sorted_tasks:
				spaces = (max_digits - len(str(task.id))) * ' '
				print task.show(spaces)
		print '=========++++++++++++=========\n'

	def close(self):
		self.conn.close()
		sys.exit()

class SQlite3_Tag(object):
	def __init__(self, item):
		self.tag_id = item[0]
		self.created = item[1]
		self.name = item[2]


def user_addTask(task_list, name=None):
	if name == None or name == "":
		new_task = raw_input('Enter name of new task: ')
		task_list.addTask(new_task)
	else:
		task_list.addTask(name)

def user_updateTask(task_list, task_id=None, status=None):
	if task_id == None or status == None:
		update_task = raw_input('Enter id of task to update: ')
		update_status = raw_input('Enter new status: ')
		task_list.updateTask(int(update_task), update_status)
	else:
		task_list.updateTask(int(task_id), status)

def user_removeTask(task_list, task_id=None):
	if task_id == None:
		del_task = raw_input('Enter id of the task to delete: ')
		task_list.removeTask(int(del_task))
	else:
		task_list.removeTask(int(task_id))

def user_renameTask(task_list, task_id=None, name=None):
	if task_id == None or name == None or name == "":
		update_task = raw_input('Enter id of task to rename: ')
		update_name = raw_input('Enter new name: ')
		task_list.renameTask(int(update_task), update_name)
	else:
		task_list.renameTask(int(task_id), name)

def shell_options(user_in, task_list):
	if user_in == 'a': 
		user_addTask(task_list),
	elif user_in == 'u':
		user_updateTask(task_list),
	elif user_in == 'r':
		user_removeTask(task_list),
	elif user_in == 's':
		return
	elif user_in == 'c':
		task_list.clearCompletedTasks()
	elif user_in == 'q':
		task_list.close()
	else:
		print 'Invalid option...'

def shell(task_list):
	print 'Welcome to To-Do-List!\n'
	while 1:
		task_list.show()
		print 'options: (a) Add Task | (u) Update Task | (x) Remove Task | (s) Show Tasks | (q) Exit'
		user_input = raw_input('What would you like to do: ')
		shell_options(user_input, task_list)

def command_options(command_line, task_list):
	user_in = command_line[2]
	if user_in == '-h' or user_in =='--help':
		print_usage()
		sys.exit()
	elif user_in == '-a' or user_in == '--add':
		try:
			user_addTask(task_list, command_line[3])
		except:
			user_addTask(task_list)
	elif user_in == '-u' or user_in == '--update':
		try:
			user_updateTask(task_list, command_line[3], command_line[4])
		except:
			user_updateTask(task_list)
	elif user_in == '-x' or user_in == '--remove':
		try:
			user_removeTask(task_list, command_line[3])
		except:
			user_removeTask(task_list)
	elif user_in == '-r' or user_in == '--rename':
		try:
			user_renameTask(task_list, command_line[3], command_line[4])
		except:
			user_renameTask(task_list)
	elif user_in == '-c' or user_in == '--clear':
		task_list.clearCompletedTasks()
	elif user_in == '-s' or user_in == '--shell':
		shell(task_list)
		return
	task_list.show()

def main():
	try:
		database_name = sys.argv[1]
	except:
		print_usage()
		sys.exit()
	
	task_list = SQlite3_TaskList(database_name)
	if len(sys.argv) > 2:
		command_options(sys.argv, task_list)
	else:
		task_list.show()


def print_usage():
	print 'Usage: todo [-achrsux] [args]\
		  \n\t<NO ARGS>          : Show Task List\
		  \n\t-a <name>          : Add Task (--add)\
		  \n\t-u <id> <status>   : Update task (--update)\
		  \n\t-x <id>            : Remove task (--remove)\
		  \n\t-r <id> <new name> : Rename task (--rename)\n\t---\
		  \n\t-c : Clear completed tasks (--clear)\
		  \n\t-s : Start shell (--shell)\
		  \n\t-n : Fresh Database (--new) WARNING! Deletes prevoious list\
		  \n\t-h : Help (--help)'

if __name__ == '__main__':
	main()