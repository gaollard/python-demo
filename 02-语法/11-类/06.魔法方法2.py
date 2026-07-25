# 魔法方法: 特殊的方法，会自动调用这个方法, 有哪些魔法方法?
# __init__: 初始化方法
# __str__: 字符串方法

# __eq__: 等于方法
# __gt__: 大于方法
# __ge__: 大于等于方法
# __lt__: 小于方法
# __le__: 小于等于方法

# __repr__: 表示方法
# __call__: 调用方法
# __getitem__: 获取方法
# __setitem__: 设置方法
# __delitem__: 删除方法
# __len__: 长度方法
# __bool__: 布尔方法
# __hash__: 哈希方法

class Car:
    def __init__(self, brand, name, price):
        self.brand = brand
        self.name = name
        self.price = price
    def __str__(self):
        return f"Car(brand={self.brand}, name={self.name})"

    def __eq__(self, other):
        return self.brand == other.brand and self.name == other.name
    
    def __gt__(self, other):
        return self.price > other.price

    def __ge__(self, other):
        return self.price >= other.price

car1 = Car('BMW', 'X5', 200)
car2 = Car('Audi', 'A6', 200)

print(car1) # Car(brand=BMW, name=X5, price=200)
print(car2) # Car(brand=Audi, name=A6, price=200)
print(car1 == car2) # False
print(car1 > car2) # True
print(car1 >= car2) # True