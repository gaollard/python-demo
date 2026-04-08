def decorator_with_args(func):
    def wrapper(*args, **kwargs):
        print(f"准备执行函数: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"函数执行完成")
        return result
    return wrapper

@decorator_with_args
def greet(name):
    print(f"Hello, {name}!")
    return f"Greeted {name}"

result = greet("Alice")


# | 符号 | 名称 | 在函数定义时 (`def`) | 在函数调用时 (`func()`) | 数据结构 |
# | :--- | :--- | :--- | :--- | :--- |
# | `*` | 单星号 | 打包位置参数 | 解包列表/元组 | 元组 (Tuple) |
# | `` | 双星号 | 打包关键字参数 | 解包字典 | 字典 (Dict) |