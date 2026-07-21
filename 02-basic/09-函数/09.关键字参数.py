def print_person(name, age, gender):
    print(f"name: {name}, age: {age}, gender: {gender}")

# 位置参数：在函数调用时，按顺序传参
print_person("张三", 18, "男")

# 关键字参数：在函数调用时，通过参数名指定参数值, 可以不按顺序传参
print_person(age=18, gender="男", name="张三")


# 位置参数和关键字参数混合使用：位置参数必须在关键字参数前面
print_person("张三", age=18, gender="男")
# print_person(name="张三", 18, "男") # SyntaxError: positional argument follows keyword argument