import sqlite3

conn = sqlite3.connect("student.db")
cur = conn.cursor()

cur.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("GInni", 20, "A"))
cur.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Don", 22, "B"))
cur.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Vishal", 21, "A"))

conn.commit()

cur.execute("SELECT * FROM students")
rows = cur.fetchall()

print("Student Records:")
for row in rows:
    print(row)

conn.close()
