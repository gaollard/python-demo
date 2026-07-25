# 实例属性：实例对象独有的属性
# 类属性：类对象独有的属性 (类对象共享的属性)

# 查找顺序：实例属性 -> 类属性

class Car:
    brand = 'BMW' # 类属性
    def __init__(self, name, price):
        # 实例属性
        self.name = name
        self.price = price

    def run(self):
        print(f'{self.brand} {self.name} is running')

car1 = Car('X5', 200)
car2 = Car('A6', 300)

print(car1.name, car1.brand) # X5 
print(car2.name, car2.brand) # A6 
print(Car.brand) # BMW