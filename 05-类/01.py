# 完善代码，让这个程序运行起来
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sit(self):
        print(self.name.title() + " is now sitting.")

    def roll_over(self):
        print(self.name.title() + " rolled over!")

my_dog = Dog('willie', 6)
my_dog.sit()
my_dog.roll_over()

class GuiBi(Dog):
    def __init__(self, name, age):
        super().__init__(name, age)
        self.color = 'red'

my_guibi = GuiBi('willie', 6)
print(my_guibi.color)