# 字符串转函数 - Python 动态函数调用示例

# 方法1: 使用 eval() 函数 (不推荐，有安全风险)
print("=== 方法1: 使用 eval() ===")

# 定义一些函数
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def greet(name):
    return f"Hello, {name}!"

# 通过字符串调用函数
func_name = "add"
result = eval(f"{func_name}(3, 5)")
print(f"eval('add(3, 5)') = {result}")

func_name = "multiply"
result = eval(f"{func_name}(4, 6)")
print(f"eval('multiply(4, 6)') = {result}")

func_name = "greet"
result = eval(f"{func_name}('World')")
print(f"eval('greet(\"World\")') = {result}")

print("\n" + "="*50 + "\n")