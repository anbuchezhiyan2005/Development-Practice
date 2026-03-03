class Employee:
    # Class attributes (global to all instances)
    company = "XYZ"

    def __init__(self, name, age): # dunder methods (methods that start and end with double underscores)
        # Instance attributes (differs between instances)
        self.name = name
        self.age = age

employee1 = Employee("alan", 24)
employee2 = Employee("bob", 21)
print("Employee 1 details:")
print(f"Name: {employee1.name}")
print(f"Age: {employee1.age}")
print(f"Company: {employee1.company}")
print("\nEmployee 2 details:")
print(f"Name: {employee2.name}")
print(f"Age: {employee2.age}")
print(f"Company: {employee2.company}")

class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage
    
    def __str__(self):
        return f"The {self.color} car has {self.mileage} miles"

car1 = Car("blue", 20000)
car2 = Car("red", 30000)
print(car1)
print(car2)
