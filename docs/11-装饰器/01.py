def simple_decorator(func):
    print("simple_decorator_call")
    def wrapper():
        print("wrapper 函数执行前")
        func()
        print("wrapper 函数执行后")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

# 调用被装饰的函数
say_hello()