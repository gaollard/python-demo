print("=== 方法2: 使用字典映射 ===")

# 创建函数字典
function_map = {
    'add': add,
    'multiply': multiply,
    'greet': greet,
    'subtract': lambda a, b: a - b,  # 匿名函数
    'divide': lambda a, b: a / b if b != 0 else "Cannot divide by zero"
}

# 通过字符串调用函数
def call_function_by_name(func_name, *args):
    if func_name in function_map:
        return function_map[func_name](*args)
    else:
        return f"Function '{func_name}' not found"

# 测试调用
print(f"call_function_by_name('add', 10, 20) = {call_function_by_name('add', 10, 20)}")
print(f"call_function_by_name('multiply', 7, 8) = {call_function_by_name('multiply', 7, 8)}")
print(f"call_function_by_name('greet', 'Python') = {call_function_by_name('greet', 'Python')}")
print(f"call_function_by_name('subtract', 15, 5) = {call_function_by_name('subtract', 15, 5)}")
print(f"call_function_by_name('divide', 20, 4) = {call_function_by_name('divide', 20, 4)}")
print(f"call_function_by_name('divide', 10, 0) = {call_function_by_name('divide', 10, 0)}")
print(f"call_function_by_name('unknown', 1, 2) = {call_function_by_name('unknown', 1, 2)}")

print("\n" + "="*50 + "\n")