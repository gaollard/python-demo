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
