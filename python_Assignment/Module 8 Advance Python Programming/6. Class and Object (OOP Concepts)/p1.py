x = 100

class Demo:
    def show(self):
        y = 50
        print("Global variable x:", x)
        print("Local variable y:", y)

d = Demo()
d.show()