"""
多继承时，两个父类的 __init__ 参数不一致会踩的坑，以及两种解法。
直接运行本文件可以看到每一步的输出。
"""

print("=== 问题一：super() 只走 MRO 的下一个类 ===")


class Father:
    def __init__(self, name):
        print("  Father.__init__ 执行了")
        self.name = name


class Mother:
    def __init__(self, age):
        print("  Mother.__init__ 执行了")
        self.age = age


class Child1(Father, Mother):
    def __init__(self, name, age):
        super().__init__(name)  # 只等价于 Father.__init__(self, name)
        self.hobby = "coding"


c1 = Child1("Tom", 18)
print("  MRO:", [cls.__name__ for cls in Child1.__mro__])
print("  name:", c1.name)
try:
    print(c1.age)
except AttributeError as e:
    print("  AttributeError:", e)  # Mother.__init__ 没执行，age 不存在


print("\n=== 问题二：父类内部也调 super() 时，参数会传给下一个父类 ===")


class Father2:
    def __init__(self, name):
        print("  Father2.__init__ 执行了")
        self.name = name
        super().__init__(name)  # MRO 里的下一个是 Mother2，它要的是 age


class Mother2:
    def __init__(self, age):
        print("  Mother2.__init__ 执行了")
        self.age = age


class Child2(Father2, Mother2):
    def __init__(self, name, age):
        super().__init__(name)


c2 = Child2("Tom", 18)
print("  name:", c2.name, "age:", c2.age)  # age 竟然是 'Tom'
# 参数个数刚好对得上，所以不报错，name 被当成 age 用了，属于更难查的静默 bug


class Mother2b:
    def __init__(self, age, city):
        self.age = age
        self.city = city


class Child2b(Father2, Mother2b):
    def __init__(self, name, age, city):
        super().__init__(name)


try:
    Child2b("Tom", 18, "SZ")
except TypeError as e:
    print("  TypeError:", e)  # 个数对不上时才会直接报错


print("\n=== 解法一：显式调用每个父类的 __init__ ===")


class Child3(Father, Mother):
    def __init__(self, name, age):
        Father.__init__(self, name)
        Mother.__init__(self, age)
        self.hobby = "coding"


c3 = Child3("Tom", 18)
print("  name:", c3.name, "age:", c3.age)
# 缺点：类名写死；若两个父类有共同基类，基类 __init__ 会被重复执行


print("\n=== 解法二：协作式 super() + **kwargs（推荐） ===")


class Father4:
    def __init__(self, name, **kwargs):
        print("  Father4.__init__ 执行了")
        self.name = name
        super().__init__(**kwargs)  # 自己认识的参数取走，剩下的继续往后传


class Mother4:
    def __init__(self, age, **kwargs):
        print("  Mother4.__init__ 执行了")
        self.age = age
        super().__init__(**kwargs)  # 最后传到 object.__init__()，此时 kwargs 为空


class Child4(Father4, Mother4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hobby = "coding"


c4 = Child4(name="Tom", age=18)
print("  MRO:", [cls.__name__ for cls in Child4.__mro__])
print("  name:", c4.name, "age:", c4.age, "hobby:", c4.hobby)
# 关键：整条 MRO 链上的类都用关键字参数 + **kwargs，且每个类都调用 super().__init__()
