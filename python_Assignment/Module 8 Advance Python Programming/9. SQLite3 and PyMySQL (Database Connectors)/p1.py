import sqlite3
conn = sqlite3.connect("student.db")

cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    grade TEXT
)
''')

print("Database and table created successfully!")

conn.commit()
conn.close()
