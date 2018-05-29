import sys,os
import curses
from curses.textpad import Textbox, rectangle
import sqlite3

VERSION = "1.0.000"
AUTHOR = "NoStress team (2018 HU-OSS B-6)"

def create_db(cur):
	table_create_sql = """CREATE TABLE if not exists Tasks (
			id integer primary key autoincrement,
			task text not null,
			due text not null,
			note text not null,
			finished integer not null);"""

	cur.execute(table_create_sql)

	table_create_sql = """CREATE TABLE if not exists TestDir1 (
			id integer primary key autoincrement,
			task text not null,
			due text not null,
			note text not null,
			finished integer not null);"""

	cur.execute(table_create_sql)

	table_create_sql = """CREATE TABLE if not exists TestDir2 (
			id integer primary key autoincrement,
			task text not null,
			due text not null,
			note text not null,
			finished integer not null);"""

	cur.execute(table_create_sql)

def getstr(stdscr, y, x, msg, colon = True, backspace_end = True, cursur_pos = 1):
	# curses.echo()
	string = msg
	cursor_x = x + len(msg)
	cursor_y = y
	cmd = 0
	while(True):
		stdscr.refresh()
		if(cmd == 8 or cmd == 127) :
			if len(string) > 1 :
				string = string[:-1]
				stdscr.addch(cursor_y, cursor_x-1, " ")
				cursor_x = cursor_x - 1
			else :
				if backspace_end:
					return ""
				elif len(string) == 1:
					string = ""
					stdscr.addch(cursor_y, cursor_x-1, " ")
					cursor_x = cursor_x - 1
		elif(cmd == 10) :
			if(colon):
				return string[1:]
			else:
				return string
		elif 32 <= cmd <= 126 :
			string = string + chr(cmd)
			cursor_x = cursor_x + 1
		elif cmd == 9 and len(string) > 7 :
			if (string[:6] == ':check'):
				conn = sqlite3.connect("lab.db")
				conn.row_factory = sqlite3.Row
				cur = conn.cursor()
				sql = "SELECT name FROM sqlite_master WHERE type='table';"
				cur.execute(sql)
				tables = cur.fetchall()
				tables.pop(1)

				sql = "select task from "+tables[cursur_pos-1][0]+" where 1"
				cur.execute(sql)
				tasks = cur.fetchall()


				task_list = []
				for t in tasks :
					task_list.append(t[0])

				target = string[7:] # Ne
				find_names = []
				for name in task_list :
					if len(name) >= len(target) and name[:len(target)] == target :
						find_names.append(name)

				if(len(find_names) == 1):
					string = string[:-len(target)]
					string = string + find_names[0]
					cursor_x = cursor_x - len(target) + len(find_names[0])
				elif(len(find_names) > 1):
					pre_result = target
					result = target
					ck = 1
					index = len(target)
					while(ck):
						for task in find_names:
							if(task[:index] != result):
								ck = 0
						if(ck != 0):
							index = index + 1
							result = find_names[0][:index]
						else :
							result = result[:-1]
							break
					string = string[:-len(target)]
					string = string + result
					cursor_x = cursor_x - len(target) + len(result)
		# :check D

		stdscr.addstr(y, x, string)
		stdscr.move(cursor_y, cursor_x)

		cmd = stdscr.getch()

def draw_menu(stdscr):
	# Initialization
	height, width = stdscr.getmaxyx()
	k = 0
	cursor_x = 0
	cursor_y = height-1
	state = 0

	# database
	conn = sqlite3.connect("lab.db")
	conn.row_factory = sqlite3.Row
	cur = conn.cursor()
	create_db(cur)

	# set up window
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.clear()
	stdscr.refresh()
	curses.start_color()
	curses.initscr()
	curses.use_default_colors()
	curses.init_pair(1, 231, 197)
	curses.init_pair(2, -1, 246) # cursur shadow
	curses.init_pair(3, -1, 252)
	# stdscr.bkgd(' ')

	# Main Loop
	while (True):
		height, width = stdscr.getmaxyx()

		# command input
		if k == ord(':'):
			command = ""
			cursor_y = height-1
			cursor_x = 1
			# stdscr.addch(height-1, 0, ':')
			# curses.echo()
			# command = stdscr.getstr(height-1, 1, 15).decode("utf-8")
			command = getstr(stdscr, height-1, 0, ":")
			# curses.noecho()
			cursor_y = height-1
			cursor_x = 0
			stdscr.move(cursor_y, cursor_x)
			# excute command
			if command == 'q':	# Quit
				break

			if len(command) > 2 and command[:2] == 'c ' and command[2:].isdigit() : # Check todo
				cur.execute('DELETE FROM todolist WHERE id=?', (command[2:],))
				conn.commit()

			if command == 'ls':  # List table
				stdscr.clear()
				stdscr.refresh()
				# editwin = curses.newwin(5,30, 2,1)
				# stdscr.attron(curses.color_pair(2))
				cmd = 0
				cursor_y = 1
				cursor_x = 1
				cursur_pos = 1;
				task_pos = 1;
				list_state = 0;
				while(True):
					curses.curs_set(0)

					# Load SQL and Initialize
					sql = "SELECT name FROM sqlite_master WHERE type='table';"
					cur.execute(sql)
					tables = cur.fetchall()
					dir_len = len(tables) - 1
					task_len = len(rows)

					# key input
					if cmd == ord('q') or cmd == curses.KEY_LEFT:
						if list_state != 0 :
							list_state = 0
							cursor_y = cursur_pos
							cursor_x = 1
					elif cmd == curses.KEY_DOWN:
						if list_state != 1 and cursor_y < dir_len:
							cursur_pos = cursur_pos + 1
							cursor_y = cursor_y + 1
						elif list_state == 1 and cursor_y < task_len:
							task_pos = task_pos + 1
							cursor_y = cursor_y + 1
					elif cmd == curses.KEY_UP:
						if list_state != 1 and cursor_y > 1:
							cursur_pos = cursur_pos - 1
							cursor_y = cursor_y - 1
						elif list_state == 1 and cursor_y > 1:
							task_pos = task_pos - 1
							cursor_y = cursor_y - 1
					elif cmd == 10 or cmd == curses.KEY_RIGHT:
						if list_state != 1 :
							list_state = 1
							task_pos = 1
							cursor_x = 22
							cursor_y = 1
					elif cmd == 27:
						if list_state != 0 :
							list_state = 0
							cursor_y = cursur_pos
							cursor_x = 1
					elif cmd == ord(':'):
						curses.curs_set(1)
						command = ""
						# cursor_y = height-1
						# cursor_x = 1
						command = getstr(stdscr, height-1, 0, ":", True, True, cursur_pos)

						# cursor_y = height-1
						# cursor_x = 0
						# stdscr.move(cursor_y, cursor_x)
						curses.curs_set(0)

						if command == 'q':
							break
						elif command == 'add':
							#reload tasks
							row_count = 1
							for row in rows :
								s = ""
								s = s + str("~ ") + str(row[1]) + " "*(43 - len(row[1]))
								s = s + row[2]
								s = s + " "*(10-len(row[2]) + 2)
								stdscr.addstr(row_count, 22, s)
								row_count = row_count + 1
							for i in range(5):
								stdscr.addstr(17+i, 22, " "*(width-2-22))

							curses.curs_set(1)
							stdscr.addstr(1+task_len, 22, "+ ")
							what = getstr(stdscr, 1+task_len, 24, "", False, False)
							stdscr.addstr(1+task_len, 22, "~ "+what)
							due = getstr(stdscr, 1+task_len, 67, "", False, False)
							stdscr.addstr(1+task_len, 67, due)
							memo = getstr(stdscr, 18, 22, "", False, False)

							tables.pop(1)
							cur.execute('INSERT INTO '+tables[cursur_pos-1][0]+' (task, due, note, finished) VALUES (?,?,?,?)', (what, due, memo, 0))
							conn.commit()
							curses.curs_set(0)

						elif len(command) >= 6 and command == 'check':
							target = command[6:]
							if (target in task_list):
								sql = "UPDATE "+tables[cursur_pos-1][0]+" SET finished = 1 WHERE task = " + target
								conn.commit()
						elif command == 'history':
							pass
						elif command == 'move':
							pass
						elif command == 'mod':
							pass


					# list_state = 0 : directory
					# list_state = 1 : tasks

					stdscr.clear()

					# Load SQL and Initialize
					sql = "SELECT name FROM sqlite_master WHERE type='table';"
					cur.execute(sql)
					tables = cur.fetchall()
					task_len = len(rows)

					# Draw Box
					rectangle(stdscr, 0, 0, height-2, width-1)
					rectangle(stdscr, 0, 0, height-2, 20)
					rectangle(stdscr, 0, 21, 15, width-1)
					rectangle(stdscr, 16, 21, height-2, width-1)
					stdscr.addstr(0,2,"Directory")
					stdscr.addstr(0,23,"Tasks")
					stdscr.addstr(16,23,"Memo")

					# print directory
					dir_index = 1
					for name in tables:
						if name[0] != 'sqlite_sequence' :
							if (cursur_pos == dir_index):
								stdscr.attron(curses.color_pair(2))
								stdscr.addstr(dir_index, 1, name[0])
								stdscr.addstr(cursur_pos, 1 + len(name[0]), " "*(19-len(name[0])))
								stdscr.attroff(curses.color_pair(2))
							else :
								stdscr.addstr(dir_index, 1, name[0])
							dir_index = dir_index + 1

					# print tasks
					tables.pop(1)
					sql = "select id, task, due, note ,finished from "+tables[cursur_pos-1][0]+" where 1"
					cur.execute(sql)

					rows = cur.fetchall()

					task_list = []
					for t in rows :
						task_list.append(t[1])

					row_count = 1
					for row in rows :
						
						s = ""
						s = s + str("~ ")
						s = s + str(row[1])
						s = s + " "*(43 - len(row[1]))
						s = s + row[2]
						s = s + " "*(10-len(row[2]) + 2)
						if (list_state == 1 and task_pos == row_count) :
							stdscr.attron(curses.color_pair(2))
							stdscr.addstr(row_count, 22, s)
							stdscr.attroff(curses.color_pair(2))
							# print memo
							stdscr.addstr(18, 22, row[3])
						else :
							stdscr.addstr(row_count, 22, s)

						row_count = row_count + 1

					stdscr.move(cursor_y, cursor_x)
					stdscr.refresh()
					cmd = stdscr.getch()


				# end loop
				cursor_y = height-1
				cursor_x = 0
				curses.curs_set(1)

			stdscr.clear()

		# cursor move
		if k == curses.KEY_DOWN:
			cursor_y = cursor_y + 1
		elif k == curses.KEY_UP:
			cursor_y = cursor_y - 1
		elif k == curses.KEY_RIGHT:
			cursor_x = cursor_x + 1
		elif k == curses.KEY_LEFT:
			cursor_x = cursor_x - 1

		# cursor binding
		cursor_x = max(0, cursor_x)
		cursor_x = min(width-1, cursor_x)

		cursor_y = max(0, cursor_y)
		cursor_y = min(height-1, cursor_y)

		# Rendering Width and Height
		# whstr = "cursor_x: {}, cursor_y: {}".format(cursor_x, cursor_y)
		# stdscr.addstr(0, 0, whstr)

		# Declaration of strings
		title = "TMI - Todo Manager Interface"
		title_version = "version " + VERSION
		title_author = "by " + AUTHOR
		title_license = "TMI is open source and freely distributable"
		title_command1 = "type    :q<Enter>             to exit"
		title_command2 = "type    :help<Enter>          to help"
		title_command3 = "type    :ls<Enter>            to list table"
		# Rendering text
		# stdscr.addstr(0, 0, title, curses.A_BOLD)

		stdscr.addstr(round(height/2 - 5), round(width/2 - len(title)/2), title, curses.A_BOLD)
		stdscr.addstr(round(height/2 - 3), round(width/2 - len(title_version)/2), title_version)
		stdscr.addstr(round(height/2 - 2), round(width/2 - len(title_author)/2), title_author)
		stdscr.addstr(round(height/2 - 1), round(width/2 - len(title_license)/2), title_license)
		stdscr.addstr(round(height/2 + 1), round(width/2 - len(title_command3)/2), title_command1)
		stdscr.addstr(round(height/2 + 2), round(width/2 - len(title_command3)/2), title_command2)
		stdscr.addstr(round(height/2 + 3), round(width/2 - len(title_command3)/2), title_command3)

		# Rendering box
		# editwin = curses.newwin(5,30, 2,1)
		# rectangle(stdscr, 2, 2, 4, 25)
		# stdscr.refresh()
		# box = Textbox(editwin)
		# box.edit()

		# Rendering table
		sql = "select id, task, due, note ,finished from Tasks where 1"
		cur.execute(sql)

		rows = cur.fetchall()

		row_count = 3
		for row in rows :
			s = ""
			s = s + str("")
			s = s + " "*(3 - len(str(row[0])))
			s = s + str(row[1])
			s = s + " "*(36 - len(row[1]))
			s = s + row[2]
			s = s + " "*(width - len(s) - 30)

			color = 3

			# stdscr.attron(curses.color_pair(color))
			# stdscr.addstr(row_count, 2, s)
			# stdscr.addstr(row_count, 0, "  ")
			# stdscr.attroff(curses.color_pair(color))
			# row_count = row_count + 1

		# after
		stdscr.move(cursor_y, cursor_x)
		stdscr.refresh()

		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

if __name__ == "__main__":
	main()