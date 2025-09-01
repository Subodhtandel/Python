class calculator:
    def __init__(self):
        self.a = 10
        self.b = 20


    def addition(self):
        print(self.a+self.b)
    
    def sub(self):
        print(self.a-self.b)
    
    def multi(self):
        print(self.a*self.b)

    def less(self):
        print(self.a<self.b)

    def div(self):
        print(self.a/self.b) 

    def gretar(self):
        print(self.a>self.b) 


c1 = calculator()
c1.sub()
c1.multi()
c1.div()
c1.less()
c1.gretar()
c1.addition()

