class emp:
    def __init__(self,id,name,email):
        self.id = id
        self.name=name
        self.email=email


    def display(self):
        print(self.id,self.name,self.email)

    def test(self):
        print(self.id)


e1 = emp(1,"self","self@gmail.com")
e1.display()
e1.test()

