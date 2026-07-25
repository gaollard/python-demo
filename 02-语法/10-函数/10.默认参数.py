def print_person(name, age, gender="男"):
    print(f"name: {name}, age: {age}, gender: {gender}")

print_person("张三", 18)
print_person("李四", 20, "女")

# 默认参数：在函数定义时，给参数设置默认值，在函数调用时，如果传入了参数值，则使用传入的参数值，否则使用默认值
# 默认参数必须放在位置参数后面
# 默认参数必须放在位置参数后面