import sys
from time import time
# To-Do-List Applet v0.1
# Progress:==========
  # Some major flaws at the moment
  # Need to consider better way to store and sort tasks
  # Need to add error handling for simple cases


# class Task
# -- A Task is something that goes on the list
# -- The App simply has a list of 
class Task(object):
	def __init__(self, name):
		self.name = name
		self.status_map = {
			0 : 'o',
			1 : '-',
			2 : 'x'
		}
		self.rev_status_map = {v : k 
			for k, v in self.status_map.iteritems()
		}
		self.status = 0
		self.created = time()
	
	def update(self, status):
		self.status = self.rev_status_map[status]

	def show(self):
		return self.status_map[self.status]

class TaskList(object):
	def __init__(self):
		self.n_tasks = 0
		self.tasks = {}

	def addTask(self, task):
		self.tasks[task.name] = task
		self.n_tasks += 1

	def removeTask(self, task_name):
		del self.tasks[task_name]
		self.n_tasks -= 1

	def show(self):
		print '\n========= To-Do-List ========='
		sorted_tasks = sorted(self.tasks.itervalues(), key=lambda task: task.created)
		for task in sorted_tasks:
			print task.show() + ' ' + task.name
		print '=========++++++++++++=========\n'

def update_task(to_do_list):
	update_task_name = raw_input('Enter the name of the task to update: ')
	update_task_status = raw_input('Enter the new status: ')
	to_do_list.tasks[update_task_name].update(update_task_status)

def remove_task(to_do_list):
	del_task_name = raw_input('Enter the name of the task to delete: ')
	to_do_list.removeTask(del_task_name)
		
def add_task(to_do_list):
	new_task_name = raw_input('Enter the name of a new task: ')
	new_task = Task(new_task_name)
	to_do_list.addTask(new_task)

def handle_options(user_input, to_do_list):
	if user_input == 'a':
		add_task(to_do_list)
	elif user_input == 'r':
		remove_task(to_do_list)
	elif user_input == 'u':
		update_task(to_do_list)
	elif user_input == 'q':
		sys.exit()

def main():
	to_do_list = TaskList()
	while 1:
		to_do_list.show()
		print '(options) a: add task | r: remove task | u: update task | q: quit'
		user_input = raw_input('What would you like to do?: ')
		handle_options(user_input, to_do_list)

if __name__ == '__main__':
	main()