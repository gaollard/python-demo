def simple_decorator(func):
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

@simple_decorator
def say_hello():
    print("Hello!")

# 调用被装饰的函数
say_hello()


class MyApp():
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.register(path, func, method="GET")
            return func
        return decorator
    def register(self, path, func, method):
        self.routes[path] = func
        print("register route:", path, "method:", method, "func:", func.__name__)

app = MyApp()

@app.get("/")
def sleep():
    print("sleep")
    return {"Hello": "World"}

# sleep()