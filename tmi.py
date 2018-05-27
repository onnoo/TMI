import sys,os
import curses
from curses.textpad import Textbox, rectangle
import sqlite3

VERSION = "1.0.000"
AUTHOR = "NoStress team (2018 HU-OSS B-6)"

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
	curses.initscr()
	curses.use_default_colors()
	curses.init_pair(1, 231, 197)
	curses.init_pair(2, 39, -1)
	curses.init_pair(3, -1, 252)
	# stdscr.bkgd(' ')

	# Loop
	while (True):
		height, width = stdscr.getmaxyx()

		# command input
		if k == ord(':'):
			command = ""
			cursor_y = height-1
			cursor_x = 1
			stdscr.addch(height-1, 0, ':')
			curses.echo()
			command = stdscr.getstr(height-1, 1, 15).decode("utf-8")
			curses.noecho()
			cursor_y = height-1
			cursor_x = 0
			stdscr.move(cursor_y, cursor_x)
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

			if command == 'ls':  # List table
				stdscr.clear()
				stdscr.refresh()
				# editwin = curses.newwin(5,30, 2,1)
				# stdscr.attron(curses.color_pair(2))
				rectangle(stdscr, 0, 0, height-2, width-1)
				rectangle(stdscr, 0, 0, height-2, 20)
				rectangle(stdscr, 0, 21, 15, width-1)
				rectangle(stdscr, 16, 21, height-2, width-1)
				stdscr.addstr(0,2,"Directory")
				stdscr.addstr(0,23,"Tasks")
				stdscr.addstr(16,23,"Memo")
				# stdscr.attroff(curses.color_pair(2))
				stdscr.refresh()
				stdscr.getch(3,3)


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
		editwin = curses.newwin(5,30, 2,1)
		# rectangle(stdscr, 2, 2, 4, 25)
		# stdscr.refresh()
		# box = Textbox(editwin)
		# box.edit()

		# Rendering table
		sql = "select id, todo, due, note ,finished from todolist where 1"
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