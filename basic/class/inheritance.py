class Animal:
    def __init__(self):
        print("animal calling...")

    def voice(self):
        print("animal callig...")


class Dog(Animal):

    def voice(self):
        print("Bhow...Bhow")

class Cat(Animal):

    def voice(self):
        print("Meow...meow")

d = Dog()
d.voice()

c = Cat()
c.voice()