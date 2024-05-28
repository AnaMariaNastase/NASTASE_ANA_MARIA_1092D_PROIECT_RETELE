import sqlite3
def init_db():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS students(
                   student_id TEXT PRIMARY KEY,
                   name TEXT NOT NULL,
                   age INTEGER NOT NULL,
                   major TEXT NOT NULL
                   )

                 '''  )
    conn.commit()
    conn.close()
init_db()
                   

