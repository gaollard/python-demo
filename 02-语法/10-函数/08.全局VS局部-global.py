num = 10

def test():
    num = 20
    print(num) # 20

test()
print(num) # 10

def test2():
    global num
    num = 30
    print(num) # 30

test2()
print(num) # 30