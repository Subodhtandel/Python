# 20: Method Overriding 

class Vehicle:
    def start(self):
        print("Vehicle is starting...")

class Car(Vehicle):
    def start(self):
        print("Car is starting with a key...")

class Bike(Vehicle):
    def start(self):
        print("Bike is starting with a button...")

v = Vehicle()
c = Car()
b = Bike()

v.start()  
c.start()   
b.start()   
