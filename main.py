import sqlite3

conn = sqlite3.connect("lab.db")
cur = conn.cursor()

def create_db():
    global conn, cur

    table_create_sql = """create table if not exists todo (
            id integer primary key autoincrement,
            what text not null,
            due text not null,
            finished integer not null);"""

    cur.execute(table_create_sql)
    conn.close()

def run_program():
	while True :
		print("Choose what to do:")
		command = input("(a: Add todo, l: List todo, m: Modify todo, c: Check, q: Quit)? ")
		print()
		if command == 'a' :
			add_todo()
		elif command == 'l' :
			list_todo()
		elif command == 'm' :
			modify_todo()
		elif command == 'c' :
                        check_todo()
		elif command == 'q' :
			break
		else :
			print()

def list_todo():
    global conn, cur

    print("Choose what do view:")
    column = input("(w: What, d: Due, f: Finished, a: All)?")
    print()

    sql = "select" + column + "from todo where 1"
    cur.execute(sql)

    rows = cur.fetchall()

    for row in rows :
        for i in range(0,len(row)) :
            if i != len(row) - 1 :
                print(row[i], end = " ")
            else :
                print(row[i])

    conn.close()


def add_todo():
    global conn, cur

    todo = input("Todo? ")
    due = input("Due date? ")

    sql = "insert into todo (what, due, finished) values ('" + todo + "', '" + due + "', '0')"
    cur.execute(sql)
    conn.commit()

    print()
    conn.close()

def modify_todo():
    list_todo()

    print()
    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    record_id = input("Record_id? ")
    todo = input("Todo? ")
    due = input("Due date? ")
    finished = input("Finished (1: yes, 0: no)? ")

    sql = "UPDATE todo SET what = '"+todo+"', due = '"+due+"', finished = "+finished+" WHERE id = "+record_id
    cur.execute(sql)
    conn.commit()

    print()
    conn.close()

def check_todo():
    list_todo()
    print()

    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    record_id = input("Record_id? ")

    sql = "UPDATE todo SET finished = " + '1' + " WHERE id = " + record_id
    cur.execute(sql)
    conn.commit()
    print("Success Change")

    print()
    conn.close()

if __name__ == "__main__":
    create_db()
    run_program()



