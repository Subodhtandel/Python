class Parent:
    def show_parent(self):
        print("This is the Parent class")

class Child1(Parent):
    def show_child1(self):
        print("This is Child1 class")

class Child2(Parent):
    def show_child2(self):
        print("This is Child2 class")

c1 = Child1()
c1.show_parent()
c1.show_child1()

c2 = Child2()
c2.show_parent()
c2.show_child2()
