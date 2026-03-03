class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"Animal {self.name}, age: {self.age}"

class Breed1(Animal):
    def __init__(self, name, age, speak):
        super().__init__(name, age)
        self.speak = speak

    def sound(self):
        print(self.speak)
    
class Breed2(Animal):
    def __init__(self, name, age, speak):
        super().__init__(name, age)
        self.speak = speak
    
    def sound(self):
        print(self.speak)

animal1 = Breed1("Cow", 4, "Moo")
animal2 = Breed2("Dog", 5, "Woof")
print(animal1)
animal1.sound()
print(animal2)
animal2.sound()

