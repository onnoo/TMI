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
        command = input("(a: Add todo, l: List todo, m: Modify todo, c: Check, s: Search, q: Quit)? ")
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
        elif command == 's' :
            search_todo()
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

    cnt = input("How many data do you want to add? (0 to return main menu) ")
    if(int(cnt) == 0) :
        print()
        return

    for i in range(0,int(cnt)) :
        todo = input("Todo? ")
        due = input("Due date? ")

        if(todo == "exit" and due == "exit") :
            i = i - 1
            break

        sql = "insert into todo (what, due, finished) values ('" + todo + "', '" + due + "', '0')"
        cur.execute(sql)
        conn.commit()
        print()

    print()
    print(str(i+1) + "/" + cnt + " data(s) completely added.")
    print()

def modify_todo():
    global conn, cur
    
    sql = "select * from todo where 1"
    cur.execute(sql)
    
    rows = cur.fetchall()
    for row in rows :
        for i in range(0,len(row)) :
            if i != len(row) - 1 :
                print(row[i], end = " ")
            else :
                print(row[i])
    print()
                
    check = False

    while True:
        record_id = input("Record_id? (0 to return main menu) ")
        if(int(record_id) == 0) :
            print()
            return
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
    global conn, cur
    
    sql = "select * from todo where 1"
    cur.execute(sql)
    
    rows = cur.fetchall()
    for row in rows :
        for i in range(0,len(row)) :
            if i != len(row) - 1 :
                print(row[i], end = " ")
            else :
                print(row[i])
    print()
    
    check = False

    while True:
        record_id = input("Record_id? (0 to return main menu) ")
        if(int(record_id) == 0) :
            print()
            return
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

def search_todo():
    global conn, cur

    search_column = input("(1. ID, 2. What, 3. Due, 4. Finished, 0. Return to main menu): ")
    search_column = int(search_column)

    if search_column == 1:
        search_word = input("ID : ")
        search_word = int(search_word)

    elif search_column == 2:
        search_word = input("What : ")

    elif search_column == 3:
        search_word = input("Due : ")

    elif search_column == 4:
        search_word = input("Finished : ")
        search_word = int(search_word)

    elif search_column == 0:
        print()
        return

    sql = "select * from todo where 1"
    cur.execute(sql)

    rows = cur.fetchall()

    print()
    for row in rows:
        if search_word == row[search_column-1]:
            for i in range(0,len(row)) :
                if i != len(row) - 1 :
                    print(row[i], end = " ")
                else :
                    print(row[i])
    print()

if __name__ == "__main__":
    create_db()
    run_program()



