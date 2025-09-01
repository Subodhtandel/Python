class A:
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def display(self):
        print(self.name,self.id)

class B(A):

    def __init__(self, id, name,phone):
        self.phone = phone
        super().__init__(id, name)

    def sample(self):
        print(self.id,self.name,self.phone)


a = A(10,"Harsh")
a.display()

b = B(20,"Hardik","798989898")
b.sample()