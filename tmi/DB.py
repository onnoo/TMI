import sqlite3
from pathlib import Path

class DB:
	def __init__(self):
		home_dir = str(Path.home())
		self.conn = sqlite3.connect(home_dir + "/data.db")
		self.cur = self.conn.cursor()

	def create_table(self, table_name):
		sql = ("CREATE TABLE if not exists {0} ("
				"id integer primary key autoincrement,"
				"what text not null,"
				"due text not null,"
				"memo text not null,"
				"finished integer not null);").format(table_name)
		self.cur.execute(sql)

	def get_table_list(self):
		sql = ("SELECT name FROM sqlite_master WHERE type='table';")
		self.cur.execute(sql)
		table_list = []
		for table in self.cur.fetchall():
			if table[0] == 'sqlite_sequence':
				continue
			table_list.append(table[0])
			return table_list
	def get_task_list(self, table_name):
		sql = ("SELECT * FROM {0} WHERE finished = 0").format(table_name)
		self.cur.execute(sql)
		task_list = self.cur.fetchall()
		return task_list

	def add_task(self, table_name, what, due, memo):
		sql = ("INSERT INTO {0} "
				"(what, due, memo, finished) VALUES (?,?,?,?)"
					).format(table_name)
		self.cur.execute(sql,(what, due, memo, 0))
		self.conn.commit()

	def mod_task(self, table_name, what ,field, value):
		sql = ('UPDATE {0} SET {1} = ? WHERE what = ?'
				).format(table_name, field)
		self.cur.execute(sql,(value, what))
		self.conn.commit()

	def get_task_name_list(self, table_name):
		sql = ("SELECT what FROM {0} WHERE finished = 0").format(table_name)
		self.cur.execute(sql)
		task_list = []
		for task in self.cur.fetchall():
			task_list.append(task[0])
		return task_list