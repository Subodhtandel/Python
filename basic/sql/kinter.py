from tkinter import *
from tkinter import ttk
import pymysql

root = Tk()
root.geometry("1080x720")

con = pymysql.connect(
    host="localhost",
    user="root",
    password="7710335010",
    port=3306,
    database="subodh"
)
cursor = con.cursor()

cols =("ID","Name","email","Phone")
table=ttk.Treeview(root,columns=cols,show="headings")
for col in cols:
    table.heading(col,text=col)
    table.place(x=10,y=300)


    

l1 = Label(root,text="username")
l1.place(x=100,y=100)

l2 = Label(root,text="email")
l2.place(x=100,y=150)

l3 = Label(root,text="Phone")
l3.place(x=100,y=200)

t1 = Entry(root)
t1.place(x=200,y=100)

t2 = Entry(root)
t2.place(x=200,y=150)

t3 = Entry(root)
t3.place(x=200,y=200)


b1 = Button (root,text="Submit",width=10)
b1.place(x=200,y=250)

root.mainloop()












# l1 = Label(root,text="Username")
# l1.grid(row=1,column=1)

# l2 = Label(root,text="email")
# l2.grid(row=2,column=1)

# l3 = Label(root,text="Phone")
# l3.grid(row=3,column=1)

# t1 = Entry(root)
# t1.grid(row=1,column=2)

# t2 = Entry(root)
# t2.grid(row=2,column=2)

# t3 = Entry(root)
# t3.grid(row=3,column=2)