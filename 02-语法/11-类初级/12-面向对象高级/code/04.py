class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

    def _private_method(self):
        print("This is a private method1")
        self.__private_method()

    def __private_method(self):
        print("This is a private method2")

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"

dog = Dog("Buddy")
print(dog.speak()) # Buddy says woof!
dog._private_method() # This is a private method1 This is a private method2
dog.__private_method() # AttributeError: 'Dog' object has no attribute '__private_method'