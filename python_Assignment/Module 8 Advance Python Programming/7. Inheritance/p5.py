class A:
    def show_a(self):
        print("This is class A")

class B(A):
    def show_b(self):
        print("This is class B")

class C(A):
    def show_c(self):
        print("This is class C")

class D(B, C):  
    def show_d(self):
        print("This is class D")

d = D()
d.show_a()
d.show_b()
d.show_c()
d.show_d()
