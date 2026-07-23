def log(*args, **kwargs):
    print("log", *args, **kwargs)

def info(*args, **kwargs):
    print("info", *args, **kwargs)

def warning(*args, **kwargs):
    print("warning", *args, **kwargs)

def error(*args, **kwargs):
    print("error", *args, **kwargs)

def critical(*args, **kwargs):
    print("critical", *args, **kwargs)

print("-------------------------------- logger --------------------------------")
print("__name__:".rjust(15), __name__)
print("__file__:".rjust(15), __file__)
print("__doc__:".rjust(15), __doc__)
print("__package__:".rjust(15), __package__)
print("__cached__:".rjust(15), __cached__)
print("__loader__:".rjust(15), __loader__)
print("__spec__:".rjust(15), __spec__)
print("__builtins__:".rjust(15), __builtins__)