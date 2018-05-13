import sqlite3

def create_db():
    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

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
            size = list_todo()
            print("number of data : " + str(size))
            print()
        elif command == 'm' :
            modify_todo()
        elif command == 'c' :
                        check_todo()
        elif command == 'q' :
            break
        else :
            print("input error")
            print()

def list_todo():
    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    size = 0

    sql = "select * from todo where 1"
    cur.execute(sql)

    rows = cur.fetchall()

    for row in rows :
        for i in range(0,len(row)) :
            if i != len(row) - 1 :
                print(row[i], end = " ")
            else :
                print(row[i])
        size = size + 1

    conn.close()

    return size

def add_todo():
    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    todo = input("Todo? ")
    due = input("Due date? ")

    sql = "insert into todo (what, due, finished) values ('" + todo + "', '" + due + "', '0')"
    cur.execute(sql)
    conn.commit()

    print()
    conn.close()

def modify_todo():
    size = list_todo()
    print()

    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    while True:
        record_id = input("Record_id? ")
        if eval(record_id) >= 1 and eval(record_id) <= size:
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
    conn.close()

def check_todo():
    size = list_todo()
    print()

    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    while True:
        record_id = input("Record_id? ")
        if eval(record_id) >= 1 and eval(record_id) <= size:
            break
        else:
            print("Input Error")
            print()

    sql = "UPDATE todo SET finished = " + '1' + " WHERE id = " + record_id
    cur.execute(sql)
    conn.commit()
    print("Success Change")

    print()
    conn.close()

if __name__ == "__main__":
    create_db()
    run_program()



