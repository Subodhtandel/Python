from tkinter import *
from tkinter import ttk
import pymysql

root = Tk()
root.geometry("500x500")

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
# show()    
def adduser():
    uname = t1.get()
    email = t1.get()
    Phone = t1.get()
    






# b1 = Button(root,text="LEFT").pack(side=LEFT)
# b2 = Button(root,text="RIGHT").pack(side=RIGHT)
# b3 = Button(root,text="TOP").pack(side=TOP)
# b4 = Button(root,text="BOTTOM").pack(side=BOTTOM)

# l1 = Label(root,text="username").grid(row=1,column=1)
# l2 = Label(root,text="email").grid(row=2,column=1)
# l3 = Label(root,text="phone").grid(row=3,column=1)

# t1 = Entry(root).grid(row=1,column=2)
# t2 = Entry(root).grid(row=2,column=2)
# t3 = Entry(root).grid(row=3,column=2)

# b1  =Button(root,text="submit").grid(row=4,column=2)



l1 = Label(root,text="username").place(x=100,y=100)
l2 = Label(root,text="email").place(x=100,y=150)
l3 = Label(root,text="phone").place(x=100,y=200)

t1 = Entry(root).place(x=200,y=100)
t2 = Entry(root).place(x=200,y=150)
t3 = Entry(root).place(x=200,y=200)

b1  =Button(root,text="submit",width=17).place(x=200,y=250)


root.mainloop()