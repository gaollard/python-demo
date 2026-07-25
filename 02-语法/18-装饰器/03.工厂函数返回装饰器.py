class MyApp():
    def __init__(self):
        self.routes = {}

    def get(self, path):
        def decorator(func):
            def wrapper(*args, **kwargs):   
                self.register(path, func, method="GET")
                result = func(*args, **kwargs)
                return func
            return wrapper
        return decorator
    def register(self, path, func, method):
        self.routes[path] = func
        print("register route:", path, "method:", method, "func:", func.__name__)

app = MyApp()

@app.get("/")
def sleep(name):
    print("sleep", name)
    return {"Hello": "World"}

sleep("tim")