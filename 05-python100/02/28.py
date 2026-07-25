# 三角形类型：判断是等边、等腰还是普通三角形。

a = float(input("请输入三角形的第一条边长: "))
b = float(input("请输入三角形的第二条边长: "))
c = float(input("请输入三角形的第三条边长: "))

if (a + b > c) and (a + c > b) and (b + c > a):
    if a == b == c:
        print("这是一个等边三角形。")
    elif a == b or a == c or b == c:
        print("这是一个等腰三角形。")
    else:
        print("这是一个普通三角形。")
else:
    print("不能构成三角形。")