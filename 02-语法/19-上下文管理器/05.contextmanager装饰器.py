from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"获取资源: {name}")
    try:
        yield name  # yield 之前的代码相当于 __enter__
    finally:
        print(f"释放资源: {name}")  # yield 之后的代码相当于 __exit__

with managed_resource("database") as res:
    print(f"使用资源: {res}")