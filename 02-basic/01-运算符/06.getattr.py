# <!-- globals() -->
# <!-- callable -->

# getattr 是 Python 的一个内置函数，它的核心作用是通过字符串的形式，动态地获取对象的属性或方法。
# 简单来说，如果说 obj.name 是静态访问（写代码时就定死了），那么 getattr(obj, "name") 就是动态访问（运行时决定获取哪个属性）。
# 它的语法结构是：getattr(对象, "属性名", 默认值)。

class Person:
    def __init__(self):
        self.name = "Alice"
        self.age = 30

p = Person()
attr_name = "name"  # 这个变量可能来自用户输入

# 等价于 p.name
print(getattr(p, attr_name))  # 输出: Alice


# 这是 getattr 最实用的功能之一。如果你尝试访问一个不存在的属性，Python 通常会报错 (AttributeError)。
# 但使用 getattr 并传入第三个参数（默认值），就可以避免报错，让代码更健壮。

class Config:
    debug = True

cfg = Config()

# 尝试获取 'timeout'，如果不存在，返回 30
timeout = getattr(cfg, "timeout", 30)

print(timeout)  # 输出: 30 (没有报错，直接给了默认值)