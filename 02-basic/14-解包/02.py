def greet(name, age):
  print(f"Hello {name}, you are {age} years old.")


# 字典解包为关键字参数
info = {"name": "Charlie", "age": 30}
greet(**info)  # 等价于 greet(name="Charlie", age=30)

# 列表解包为位置参数
args = ["David", 28]
greet(*args)  # 等价于 greet("David", 28)
