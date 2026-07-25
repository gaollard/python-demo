# 嵌套函数：在函数内部定义的函数

def outer():
    print("outer called")

    def inner():
        print("inner called")

    def inner2():
        print("inner2 called")

    inner2()

    return inner

outer()()