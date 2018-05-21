import sys,os
import curses
import sqlite3

def create_db(cur):
	table_create_sql = """create table if not exists todolist (
			id integer primary key autoincrement,
			todo text not null,
			due text not null,
			note text not null,
			finished integer not null);"""

	cur.execute(table_create_sql)

def draw_menu(stdscr):
	# Initialization
	height, width = stdscr.getmaxyx()
	k = 0
	cursor_x = 0
	cursor_y = height-1
	state = 0

	# database
	conn = sqlite3.connect("lab.db")
	cur = conn.cursor()
	create_db(cur)

	# set up window
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.clear()
	stdscr.refresh()
	curses.start_color()
	curses.use_default_colors()
	# curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	# curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
	# curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
	stdscr.bkgd(' ')

	# Loop
	while (True):
		height, width = stdscr.getmaxyx()

		# command input
		if k == ord(':'):
			command = ""
			d = 0
			cursor_y = height-1
			cursor_x = 1

			while (d != 10):
				stdscr.addch(height-1, 0, ':')

				if d != 0:
					if d == 8 or d == 127:
						if len(command) != 0 :
							command = command[:-1]
							stdscr.delch(cursor_y, cursor_x-1)
							cursor_x = cursor_x - 1
					else:
						command = command + chr(d)
						cursor_x = cursor_x + 1

				stdscr.addstr(cursor_y, 1, command)

				stdscr.move(cursor_y, cursor_x)

				d = stdscr.getch()

			cursor_x = 0
			cursor_y = height-1
			# excute command
			if command == 'q':	# Quit
				break
			if command == 'a':	# Add todo
				# Rendering text
				stdscr.clear()
				stdscr.refresh()
				stdscr.addstr(0, 0, "Todo : ")
				stdscr.addstr(1, 0, "Due  : ")
				stdscr.addstr(2, 0, "Note : ")

				# User input
				curses.echo()
				todo = stdscr.getstr(0, 7, 15).decode("utf-8")
				due = stdscr.getstr(1, 7, 15).decode("utf-8")
				note = stdscr.getstr(2, 7, 15).decode("utf-8")
				curses.noecho()

				# Excute sql
				cur.execute('insert into todolist (todo, due, note, finished) values (?,?,?,?)', (todo, due, note, 0))
				conn.commit()

				aa = stdscr.getch()

			if len(command) > 2 and command[:2] == 'c ' and command[2:].isdigit() : # Check todo
				cur.execute('DELETE FROM todolist WHERE id=?', (command[2:],))
				conn.commit()

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
		title = "Xnen : Todo - List"
		subtitle = "Command >>> ':' + a(add), c(check), q(quit)"

		# Rendering text
		stdscr.addstr(0, 0, title, curses.A_BOLD)
		stdscr.addstr(1, 0, subtitle, curses.A_BOLD)

		# Rendering table
		sql = "select id, todo, due, note ,finished from todolist where 1"
		cur.execute(sql)

		rows = cur.fetchall()

		row_count = 3
		for row in rows :
			s = ""
			for i in range(0, len(row)) :
				s = s + str(row[i]) + "\t"
			stdscr.addstr(row_count, 0, s)
			row_count = row_count + 1

		# after
		stdscr.move(cursor_y, cursor_x)
		stdscr.refresh()

		k = stdscr.getch()

def main():
	curses.wrapper(draw_menu)

if __name__ == "__main__":
	main()