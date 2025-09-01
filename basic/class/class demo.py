class Test:
    clg="ABC"

    def __init__(self,id,name):
        self.id=id
        self.name=name

    def display(self):
        print(self.id,self.name,self.clg)

    # def display(self):
    #     self.id=12
    #     self.clg="ABD"
    #     print(self.id,self.clg)

    @classmethod
    def run(self):
        self.id=34
        self.clg="ACD"
        print(self.id,self.clg)

t1=Test(12,"ABC")
t1.display()
Test.run()
t1.display()