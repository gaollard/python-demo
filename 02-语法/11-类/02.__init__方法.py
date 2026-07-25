# __init__ 方法是一个特殊的方法，当创建一个对象时，会自动调用这个方法
# 它用于初始化对象的属性
# 它必须包含 self 参数，并且是第一个参数
# 它必须包含所有的属性
# 它必须包含所有的方法
# 它必须包含所有的参数
# 它必须包含所有的返回值
# 它必须包含所有的异常
# 它必须包含所有的日志
# 它必须包含所有的调试

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print("Dog 类初始化")

    def sit(self):
        print(self.name.title() + " is now sitting.")

    def roll_over(self):
        print(self.name.title() + " rolled over!")

my_dog = Dog('willie', 6)
my_dog.sit()
my_dog.roll_over()