import core.logger as logger
# 一个文件就是一个模块
# 模块有哪些内置变量

# 字符串长度对其的方式

# 字符串长度对其的方式
print("--------------------------------")
print("__name__:".rjust(15), __name__)
print("__file__:".rjust(15), __file__)
print("__doc__:".rjust(15), __doc__)
print("__package__:".rjust(15), __package__)
print("__cached__:".rjust(15), __cached__)
print("__loader__:".rjust(15), __loader__)
print("__spec__:".rjust(15), __spec__)
print("__builtins__:".rjust(15), __builtins__)

logger.log("test")