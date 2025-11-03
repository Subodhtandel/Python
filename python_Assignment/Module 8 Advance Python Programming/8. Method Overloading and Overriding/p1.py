#19: Method Overloading
class MathOperations:
    def add(self, *args):
        total = 0
        for num in args:
            total += num
        return total

math = MathOperations()
print("Add two numbers:", math.add(5, 10))
print("Add three numbers:", math.add(1, 2, 3))
print("Add five numbers:", math.add(2, 4, 6, 8, 10))
