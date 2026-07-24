# 继承：子类可以复用父类的属性和方法
# 子类可以新增自己的属性和方法，也可以重写父类方法
# super()：调用父类的方法

class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f'{self.name} is eating')

    def sleep(self):
        print(f'{self.name} is sleeping')


# Dog 继承 Animal
class Dog(Animal):
    def __init__(self, name, breed):
        # 调用父类 __init__，初始化 name
        super().__init__(name)
        # 子类自己的属性
        self.breed = breed

    # 重写父类方法
    def eat(self):
        print(f'{self.name} ({self.breed}) is eating bones')

    # 子类新增方法
    def bark(self):
        print(f'{self.name} is barking: woof!')


dog = Dog('Willie', 'Husky')
dog.eat()      # Willie (Husky) is eating bones  —— 调用子类重写后的方法
dog.sleep()    # Willie is sleeping              —— 继承自父类
dog.bark()     # Willie is barking: woof!        —— 子类自己的方法
print(dog.name, dog.breed)  # Willie Husky

# isinstance / issubclass
print(isinstance(dog, Dog))      # True
print(isinstance(dog, Animal))   # True  —— 子类实例也是父类的实例
print(issubclass(Dog, Animal))   # True
