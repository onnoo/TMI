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

def run_program():
    while True :
        print("Choose what to do:")
        command = input("(a: Add todo, l: List todo, m: Modify todo, c: Check, q: Quit)? ")
        print()
        if command == 'a' :
            add_todo()
        elif command == 'l' :
            size = list_todo()
            print("number of data : " + str(size))
            print()
        elif command == 'm' :
            modify_todo()
        elif command == 'c' :
            check_todo()
        elif command == 'q' :
            conn.close()
            break
        else :
            print("input error")
            print()

def list_todo():
    global conn, cur

    print("Choose what do view:")
    column = input("w: What, d: Due, f: Finished, a: All)? ")
    print()

    if column == 'w' :
        column = "what"
    elif column == 'd' :
        column = "due"
    elif column == 'f':
        column = "finished"
    elif column == 'a':
        column = "what, due, finished"

    size = 0

    sql = "select " + "id," + column + " from todo where 1"
    cur.execute(sql)

    rows = cur.fetchall()

    for row in rows :
        for i in range(0,len(row)) :
            if i != len(row) - 1 :
                print(row[i], end = " ")
            else :
                print(row[i])
        size = size + 1

    return size

def add_todo():
    global conn, cur

    todo = input("Todo? ")
    due = input("Due date? ")

    sql = "insert into todo (what, due, finished) values ('" + todo + "', '" + due + "', '0')"
    cur.execute(sql)
    conn.commit()

    print()

def modify_todo():
    list_todo()
    print()

    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    sql = "select * from todo where 1"
    cur.execute(sql)
    
    rows = cur.fetchall()
    check = False

    while True:
        record_id = input("Record_id? ")
        for row in rows:
            if eval(record_id) == row[0]:
                check = True
                break
            else:
                check = False
        if check == True:
            break
        else:
            print("Input Error")
            print()

    todo = input("Todo? ")
    due = input("Due date? ")

    while True:
        finished = input("Finished (1: yes, 0: no)? ")
        if eval(finished) == 0 or eval(finished) == 1:
            break
        else:
            print("Input Error: you should input only 0 or 1")
            print()

    sql = "UPDATE todo SET what = '"+todo+"', due = '"+due+"', finished = "+finished+" WHERE id = "+record_id
    cur.execute(sql)
    conn.commit()

    print()

def check_todo():
    size = list_todo()
    print()

    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()
    
    sql = "select * from todo where 1"
    cur.execute(sql)
    
    rows = cur.fetchall()
    check = False

    while True:
        record_id = input("Record_id? ")
        for row in rows:
            if eval(record_id) == row[0]:
                check = True
                break
            else:
                check = False
        if check == True:
            break
        else:
            print("Input Error")
            print()

    sql = "UPDATE todo SET finished = " + '1' + " WHERE id = " + record_id
    cur.execute(sql)
    conn.commit()
    print("Success Change")

    print()

if __name__ == "__main__":
    create_db()
    run_program()



