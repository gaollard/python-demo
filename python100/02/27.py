# 三角形判断：输入三边长，判断能否构成三角形。

a = float(input("请输入三角形的第一条边长: "))
b = float(input("请输入三角形的第二条边长: "))
c = float(input("请输入三角形的第三条边长: "))

if (a + b > c) and (a + c > b) and (b + c > a):
    print("可以构成三角形。")
else:
    print("不能构成三角形。")