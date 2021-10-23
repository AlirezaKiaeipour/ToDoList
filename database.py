import sqlite3

con = sqlite3.connect("database.db")
data = con.cursor()

def select():
    data.execute("SELECT * FROM task")
    result = data.fetchall()
    return result

def mark(i):
    data.execute(f'UPDATE task SET mark=1 WHERE title="{i}"')
    con.commit()

def delete(i):
    data.execute(f'DELETE FROM task WHERE title = "{i}"')
    con.commit()

def add(title,description,date,time,important):
    data.execute(f'INSERT INTO task(title,description,date,time,import) VALUES ("{title}","{description}","{date}","{time}","{important}")')
    con.commit()