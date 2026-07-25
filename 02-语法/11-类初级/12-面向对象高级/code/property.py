class Person:
    def __init__(self, name, age):
        self.name = name
        self.__age = age

    @property
    def age(self):
        """对外只读（或可在 setter 里校验）"""
        return self.__age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("年龄不能为负")
        self.__age = value

p = Person("Alice", 20)
print(p.age)   # 20 —— 像访问属性，实际走 getter
p.age = 25     # 走 setter，可做校验
# p.age = -1   # ValueError