import curses
from curses.textpad import Textbox, rectangle



class Room:
	
	def __init__(self, stdscr, roomManager):
		self.stdscr = stdscr
		self.height, self.width = stdscr.getmaxyx()
		self.cursor_x = 0
		self.cursor_y = self.height-1
		self.rm = roomManager
		self.command = ""
		self.command_check = False

	def get_command(self):
		if self.key == ord(':') and not self.command_check:
			self.command = ":"
			self.command_check = True
			self.cursor_x = self.cursor_x + 1
		elif self.command_check:
			if self.key == 10:
				self.command_check = False
				self.cursor_x = 0
				tmp = self.command[1:]
				self.command = ""
				return tmp
			elif self.key == 8 or self.key == 127:
				if len(self.command) == 1:
					self.command_check = False
					self.cursor_x = 0
					self.command = ""
				else:
					self.command = self.command[:-1]
					self.cursor_x = self.cursor_x - 1
			elif 32 <= self.key <= 126:
				self.command = self.command + chr(self.key)
				self.cursor_x = self.cursor_x + 1

	def logic(self):
		pass
	def render(self):
		pass
	def get_key(self):
		pass

class TitleRoom(Room):

	def __init__(self, stdscr, roomManager, version, author):
		super(TitleRoom, self).__init__(stdscr, roomManager)
		self.name = "DefaultRoom"
		self.title = [
		"TMI - Task Manager Interface",
		"",
		"version " + version,
		"by " + author,
		"TMI is open source and freely distributable",
		"",
		"type    :q<Enter>             to exit      ",
		"type    :help<Enter>          to help      ",
		"type    :ls<Enter>            to list table"
		]
		self.key = 0

	def logic(self):
		execute = self.get_command()
		if execute == 'q':
			self.rm.stop()
		elif execute == 'ls':
			self.rm.set_room("TableRoom")
		elif execute == 'help':
			self.rm.set_room("HelpRoom")


	def render(self):
		self.stdscr.clear()
		self.stdscr.move(self.cursor_y, self.cursor_x)
		
		row_num = 0
		for text in self.title:
			if row_num == 0:
				self.stdscr.attron(curses.A_BOLD)
			else:
				self.stdscr.attroff(curses.A_BOLD)

			self.stdscr.addstr(round(self.height/2 - 5 + row_num), \
			round(self.width/2 - len(text)/2), text)
			row_num = row_num + 1

		self.stdscr.addstr(self.cursor_y, 0, self.command)

		self.stdscr.refresh()

	def get_key(self):
		if self.rm.ready != 0:
			self.key = self.stdscr.getch()

class TableRoom(Room):

	def __init__(self, stdscr, roomManager, db):
		super(TableRoom, self).__init__(stdscr, roomManager)
		self.name = "TableRoom"
		self.db = db
		self.key = 0
		self.string = ""
		self.string_x = 1
		self.dir_cursor = 1
		self.task_cursor = 1
		self.table_list = self.db.get_table_list()
		if len(self.table_list) != 0:
			self.current_table = self.table_list[self.dir_cursor-1]
			self.task_list = self.db.get_task_list(self.current_table)
		else:
			self.current_table = 0
			self.task_list = []
		
		self.in_table = False
		self.string_check = False
		self.add_dir = False
		self.add_task = 0
		self.add_task_on = False
		self.what = ""
		self.due = ""
		self.memo = ""

	def logic(self):
		in_table = self.in_table
		
		execute = self.get_command()
		string = self.get_string(self.cursor_y, self.cursor_x)
		
		if self.key == curses.KEY_DOWN:
			if not in_table and self.dir_cursor < len(self.table_list):
				self.dir_cursor = self.dir_cursor + 1
			elif in_table and self.task_cursor < len(self.task_list):
				self.task_cursor = self.task_cursor + 1
		elif self.key == curses.KEY_UP:
			if not in_table and self.dir_cursor > 1:
				self.dir_cursor = self.dir_cursor - 1
			elif in_table and self.task_cursor > 1:
				self.task_cursor = self.task_cursor - 1
		elif self.key == curses.KEY_RIGHT:
			if not in_table:
				self.in_table = True
				self.task_cursor = 1
		elif self.key == curses.KEY_LEFT:
			if in_table:
				self.in_table = False


		if execute == 'q':
			self.rm.set_room("DefaultRoom")
		elif execute == 'add -d':
			if self.string_check == False:
				self.string_check = True
				self.cursor_y = 1+len(self.table_list)
				self.cursor_x = 1
				self.string_x = 1
		elif execute == 'add':
			if self.string_check == False:
				self.string_check = True
				self.add_task = 1
				self.cursor_y = 1+len(self.task_list)
				self.cursor_x = 24
				self.string_x = 22
				self.string = "+ "
		elif len(execute) >= 6 and execute[:6] == "check ":
			target = execute[6:]
			if target in self.db.get_task_name_list(self.current_table):
				self.db.mod_task(self.current_table, target , 'finished', 1)

		if self.add_dir:
			try:
				self.db.create_table(string)
				string = ""
				self.add_dir = False
			except:
				pass

		if self.add_task == 3:
			self.memo = self.string

		if self.add_task_on == True:
			if self.add_task == 2:
				self.what = string
			elif self.add_task == 3:
				self.due = string
			elif self.add_task == 0:
				self.memo = string
				self.db.add_task(self.current_table, self.what, self.due, self.memo)
				self.what = ""
				self.due = ""
				self.memo = ""
			self.add_task_on = False
			string = ""



		self.table_list = self.db.get_table_list()
		if len(self.table_list) != 0:
			self.current_table = self.table_list[self.dir_cursor-1]
			self.task_list = self.db.get_task_list(self.current_table)
		else:
			self.current_table = 0
			self.task_list = []

	def render(self):
		if self.command_check == False and self.string_check == False and self.add_task == 0:
			curses.curs_set(0)
		else:
			curses.curs_set(1)
		stdscr = self.stdscr
		height = self.height
		width = self.width
		dir_cursor = self.dir_cursor

		stdscr.clear()

		rectangle(stdscr, 0, 0, height-2, width-1)
		rectangle(stdscr, 0, 0, height-2, 20)
		rectangle(stdscr, 0, 21, 15, width-1)
		rectangle(stdscr, 16, 21, height-2, width-1)
		stdscr.addstr(0,2,"Directory")
		stdscr.addstr(0,23,"Tasks")
		stdscr.addstr(16,23,"Memo")

		table_pos_y = 1
		for table_name in self.table_list:
			if not self.string_check and dir_cursor == table_pos_y:
				stdscr.attron(curses.color_pair(1))
				stdscr.addstr(table_pos_y, 1, table_name)
				stdscr.addstr(table_pos_y, 1 + len(table_name), " "*(19-len(table_name)))
				stdscr.attroff(curses.color_pair(1))
			else:
				stdscr.addstr(table_pos_y, 1, table_name)
			table_pos_y = table_pos_y + 1

		task_pos_y = 1
		for task in self.task_list:
			if task[4] == 1:
				continue
			s = ""
			s = s + str("~ ") + str(task[1]) + " "*(43 - len(task[1]))
			s = s + task[2]
			s = s + " "*(10-len(task[2]) + 2)
			if self.add_task == 0 and self.in_table and self.task_cursor == task_pos_y:
				stdscr.attron(curses.color_pair(1))
				stdscr.addstr(task_pos_y, 22, s)
				stdscr.attroff(curses.color_pair(1))
				stdscr.addstr(18, 22, task[3])
			else:
				stdscr.addstr(task_pos_y, 22, s)
			task_pos_y = task_pos_y + 1

		
		if self.string_check:
			self.stdscr.addstr(self.cursor_y, self.string_x, self.string)
		else:
			self.stdscr.addstr(self.cursor_y, 0, self.command)
		if self.add_task > 0:
			for i in range(5):
				stdscr.addstr(17+i, 22, " "*(width-2-22))
			self.stdscr.addstr(1+len(self.task_list), 22, "+ "+self.what)
			self.stdscr.addstr(1+len(self.task_list), 67, self.due)
			self.stdscr.addstr(18, 22, self.memo)

		stdscr.move(self.cursor_y, self.cursor_x)

	def get_key(self):
		if self.rm.ready != 0:
			self.key = self.stdscr.getch()

	def get_string(self, y, x):
		self.cursor_x = x
		self.cursor_y = y
		if self.string_check:
			if self.key == 10:
				if self.string_check == True and self.add_task == 0:
					self.string_check = False
					self.cursor_x = 0
					self.cursor_y = self.height-1
					tmp = self.string
					self.string = ""
					self.add_dir = True
					return tmp
				elif self.add_task == 1:
					self.add_task = 2
					self.cursor_x = 67
					self.string_x = 67
					self.cursor_y = self.cursor_y
					tmp = self.string[2:]
					self.string = ""
					self.add_task_on = True
					return tmp
				elif self.add_task == 2:
					self.add_task = 3
					self.cursor_x = 22
					self.string_x = 22
					self.cursor_y = 18
					tmp = self.string
					self.string = ""
					self.add_task_on = True
					return tmp
				elif self.add_task == 3:
					self.add_task = 0
					self.cursor_x = 0
					self.cursor_y = self.height-1
					tmp = self.string
					self.string = ""
					self.add_task_on = True
					self.string_check = False
					return tmp

			elif self.key == 8 or self.key == 127:
				if len(self.string) > 0:
					self.cursor_x = self.cursor_x - 1
					self.string = self.string[:-1]
			elif 32 <= self.key <= 126:
				self.string = self.string + chr(self.key)
				self.cursor_x = self.cursor_x + 1
		return ""

	def get_command(self):
		if self.key == ord(':') and not self.command_check:
			self.command = ":"
			self.command_check = True
			self.cursor_x = self.cursor_x + 1
		elif self.command_check:
			if self.key == 10:
				self.command_check = False
				self.cursor_x = 0
				tmp = self.command[1:]
				self.command = ""
				return tmp
			elif self.key == 8 or self.key == 127:
				if len(self.command) == 1:
					self.command_check = False
					self.cursor_x = 0
					self.command = ""
				else:
					self.command = self.command[:-1]
					self.cursor_x = self.cursor_x - 1
			elif 32 <= self.key <= 126:
				self.command = self.command + chr(self.key)
				self.cursor_x = self.cursor_x + 1
			elif self.key == 9 and len(self.command) > 7:
				if self.command[:6] == ":check":
					task_list = self.db.get_task_name_list(self.current_table)
					# self.stdscr.addstr(4,4,task_list[0])
					target = self.command[7:]
					find_tasks = []
					for task in task_list:
						if len(task) >= len(target) and task[:len(target)] == target:
							find_tasks.append(task)

					if len(find_tasks) == 1:
						self.command = self.command[:-len(target)]
						self.command = self.command + find_tasks[0]
						self.cursor_x = self.cursor_x - len(target) + len(find_tasks[0])
					elif len(find_tasks) > 1:
						pre_result = target
						result = target
						ck = True
						index = len(target)
						while ck:
							for task in find_tasks:
								if task[:index] != result:
									ck = False
							if ck != False:
								index = index + 1
								result = find_tasks[0][:index]
							else:
								result = result[:-1]
								break
						self.command = self.command[:-len(target)]
						self.command = self.command + result
						self.cursor_x = self.cursor_x - len(target) + len(result)
		return ""

class HelpRoom(Room):
	def __init__(self, stdscr, roomManager):
		super(HelpRoom, self).__init__(stdscr, roomManager)
		self.name = "HelpRoom"
		self.help = [
							"User Manuals",
							"\n",
							"\n",
							"Name",
							"	tmi - task manage interface.",
							"	",
							"How to use",
							"	tmi [:add] add task(due, memo)",
							"	tmi [:check] update finished to 1",
							"	",
							"Explain",
							"	TMI is a TUI program using curses package. You can save tasks for", 
							"	each directory and you can write notes on each task.",
							"	",
							"Options",
							"	 [:add -d] add directory",
							"	",
							"Author",
							"     No stress team (2018 HU-OSS B-6)",
					]
		self.k = 0

	def logic(self):
		execute = self.get_command()

		if execute == 'q':
			self.rm.set_room("DefaultRoom")

	def render(self):
		self.stdscr.clear()

		line = 0
		for text in self.help:
			if line == 0:
				self.stdscr.attron(curses.A_BOLD)
				self.stdscr.addstr(line + 2, round(self.width/2 - len(self.help[0])/2), text)
				line = line + 1
				continue
			else:
				self.stdscr.attroff(curses.A_BOLD)
			
			self.stdscr.addstr(line + 3, 0, text)

			line = line + 1

		self.stdscr.addstr(self.cursor_y, 0, self.command)

		self.stdscr.refresh()

	def get_key(self):
		if self.rm.ready != 0:
			self.key = self.stdscr.getch()