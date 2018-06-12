import sys,os
import curses
import click
from DB import DB
from RoomManager import RoomManager
from Room import TitleRoom, TableRoom, HelpRoom


VERSION = "0.6.608"
AUTHOR = "NoStress team (2018 HU-OSS B-6)"

# Command Line
def version(ctx, param, value):
	if not value or ctx.resilient_parsing:
		return
	click.echo('tmi version : ' + VERSION)
	ctx.exit()


# Text User Interface

@click.command()
@click.option('--version', is_flag=True, callback=version,
              expose_value=False, is_eager=True, help='Show what version')
def main():
	curses.wrapper(run)
	

def run(stdscr):
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.start_color()
	curses.initscr()
	curses.use_default_colors()
	curses.init_pair(1, -1, 246)

	db = DB()
	rm = RoomManager()
	rm.add_room(TitleRoom(stdscr, rm, VERSION, AUTHOR))
	rm.add_room(TableRoom(stdscr, rm, db))
	rm.add_room(HelpRoom(stdscr, rm))

	rm.start()

if __name__ == "__main__":
	main()