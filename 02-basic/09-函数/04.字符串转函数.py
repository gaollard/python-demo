# 方法3: 使用 getattr() 和模块
print("=== 方法3: 使用 getattr() ===")

import math

# 数学函数映射
math_functions = {
    'sqrt': math.sqrt,
    'sin': math.sin,
    'cos': math.cos,
    'log': math.log,
    'pow': math.pow
}

def call_math_function(func_name, *args):
    if func_name in math_functions:
        return math_functions[func_name](*args)
    else:
        return f"Math function '{func_name}' not found"

# 测试数学函数
print(f"call_math_function('sqrt', 16) = {call_math_function('sqrt', 16)}")
print(f"call_math_function('sin', math.pi/2) = {call_math_function('sin', math.pi/2)}")
print(f"call_math_function('pow', 2, 3) = {call_math_function('pow', 2, 3)}")

print("\n" + "="*50 + "\n")

# 方法4: 动态创建函数
print("=== 方法4: 动态创建函数 ===")

def create_function_from_string(func_name, operation):
    """根据字符串动态创建函数"""
    if operation == 'add':
        def dynamic_func(a, b):
            return a + b
    elif operation == 'multiply':
        def dynamic_func(a, b):
            return a * b
    elif operation == 'power':
        def dynamic_func(a, b):
            return a ** b
    else:
        def dynamic_func(a, b):
            return f"Unknown operation: {operation}"
    
    # 设置函数名
    dynamic_func.__name__ = func_name
    return dynamic_func

# 创建动态函数
add_func = create_function_from_string('my_add', 'add')
multiply_func = create_function_from_string('my_multiply', 'multiply')
power_func = create_function_from_string('my_power', 'power')

print(f"add_func(5, 3) = {add_func(5, 3)}")
print(f"multiply_func(4, 7) = {multiply_func(4, 7)}")
print(f"power_func(2, 8) = {power_func(2, 8)}")
print(f"add_func.__name__ = {add_func.__name__}")

print("\n" + "="*50 + "\n")

# 方法5: 使用 exec() 动态执行代码
print("=== 方法5: 使用 exec() ===")

def create_function_with_exec(func_name, operation):
    """使用 exec 动态创建函数"""
    code = f"""
def {func_name}(a, b):
    return a {operation} b
"""
    local_vars = {}
    exec(code, globals(), local_vars)
    return local_vars[func_name]

# 创建函数
plus_func = create_function_with_exec('plus', '+')
minus_func = create_function_with_exec('minus', '-')
times_func = create_function_with_exec('times', '*')

print(f"plus_func(10, 5) = {plus_func(10, 5)}")
print(f"minus_func(10, 5) = {minus_func(10, 5)}")
print(f"times_func(10, 5) = {times_func(10, 5)}")

print("\n" + "="*50 + "\n")

# 方法6: 实际应用场景 - 计算器
print("=== 方法6: 实际应用 - 简单计算器 ===")

class Calculator:
    def __init__(self):
        self.operations = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else "Error: Division by zero",
            '**': lambda a, b: a ** b,
            '%': lambda a, b: a % b if b != 0 else "Error: Modulo by zero"
        }
    
    def calculate(self, expression):
        """计算表达式，格式: 'a operator b'"""
        try:
            parts = expression.split()
            if len(parts) != 3:
                return "Error: Invalid expression format"
            
            a, operator, b = parts
            a, b = float(a), float(b)
            
            if operator in self.operations:
                return self.operations[operator](a, b)
            else:
                return f"Error: Unknown operator '{operator}'"
        except ValueError:
            return "Error: Invalid number format"
        except Exception as e:
            return f"Error: {str(e)}"

# 使用计算器
calc = Calculator()
expressions = [
    "10 + 5",
    "10 - 5", 
    "10 * 5",
    "10 / 5",
    "2 ** 3",
    "10 % 3",
    "10 / 0",
    "10 % 0",
    "10 unknown 5",
    "invalid expression"
]

for expr in expressions:
    result = calc.calculate(expr)
    print(f"{expr} = {result}")

print("\n" + "="*50 + "\n")

# 方法7: 使用 functools.partial
print("=== 方法7: 使用 functools.partial ===")

from functools import partial

def create_partial_function(func_name, base_func, *args):
    """创建偏函数"""
    partial_func = partial(base_func, *args)
    partial_func.__name__ = func_name
    return partial_func

# 创建偏函数
add_5 = create_partial_function('add_5', add, 5)
multiply_3 = create_partial_function('multiply_3', multiply, 3)

print(f"add_5(10) = {add_5(10)}")  # 相当于 add(5, 10)
print(f"multiply_3(7) = {multiply_3(7)}")  # 相当于 multiply(3, 7)

print("\n" + "="*50 + "\n")

# 总结
print("=== 总结 ===")
print("1. eval() - 简单但不安全，不推荐在生产环境使用")
print("2. 字典映射 - 最推荐的方法，安全且高效")
print("3. getattr() - 适合访问模块中的函数")
print("4. 动态创建函数 - 适合需要运行时创建函数的场景")
print("5. exec() - 功能强大但需要谨慎使用")
print("6. 实际应用 - 计算器、插件系统等")
print("7. functools.partial - 创建预设参数的函数")
