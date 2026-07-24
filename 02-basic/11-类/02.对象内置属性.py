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

# __dict__ 属性返回一个字典，包含了对象的所有属性
print(my_dog.__dict__)

# __class__ 属性返回对象的类
print(my_dog.__class__) # <class '__main__.Dog'>

# __module__ 属性返回对象所属的模块
print(my_dog.__module__) # __main__

# __doc__ 属性返回对象的文档字符串
print(my_dog.__doc__) # None