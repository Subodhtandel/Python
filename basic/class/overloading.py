from multipledispatch import dispatch

class calc:
    @dispatch(int,int)
    def add(self,a,b):
        print(f"Addition is {a+b}")

    @dispatch(int,int,int)
    def add(self,a,b,c):
        print(f"Addition is {a+b+c}")

    @dispatch(float,int)
    def add(self,a,b):
        print(f"Addition is {a+b}")


# def calc(self,*a):
#         sum=0
#         for i in a:
#             sum+=i
#         print(f"Addition is {sum}")

c=calc()
c.add(10,20)
c.add(10,20,30)
c.add(10.0,20)