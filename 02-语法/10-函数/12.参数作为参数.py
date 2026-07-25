def execute_func(func, *args, **kwargs):
    return func(*args, **kwargs)

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

print(execute_func(add, 1, 2))
print(execute_func(sub, 1, 2))

# 3
# -1

# 参数作为参数：在函数调用时，将函数作为参数传入另一个函数
# 参数作为参数：在函数调用时，将函数作为参数传入另一个函数