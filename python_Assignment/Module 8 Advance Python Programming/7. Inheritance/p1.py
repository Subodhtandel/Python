class Parent:
    def show_parent(self):
        print("This is the Parent class")

class Child(Parent):  
    def show_child(self):
        print("This is the Child class")

c = Child()
c.show_parent()
c.show_child()
