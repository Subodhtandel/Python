import sqlite3

db = sqlite3.connect("database.db")
# db.execute("create table student(id int primary key,name varchar(20),email varchar(30))")

# db.execute("insert into student values(1,'Harsh','harsh@gmail.com')")
# db.execute("insert into student values(2,'Sameer','sameer@gmail.com')")
# db.execute("insert into student values(3,'kirit','kirit@gmail.com')")
# db.execute("insert into student values(4,'Sam','sam@gmail.com')")
# db.execute("update student set name='Harsh Kumar',email='harshk@gmail.com' where id=1")
# db.execute("delete from student where id=3")
db.commit()
data = db.execute("select * from student")
dt =  data.fetchall()
for i in dt:
   for k in i:
      print(k)