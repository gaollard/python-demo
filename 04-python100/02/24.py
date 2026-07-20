# 成绩评级：根据分数输出 A/B/C/D/F 等级。

grade=int(input("请输入成绩（0-100）："))

if grade >= 90:
    print("成绩等级为 A")
elif grade >= 80:
    print("成绩等级为 B")
elif grade >= 70:   
    print("成绩等级为 C")
elif grade >= 60:
    print("成绩等级为 D")
else:
    print("成绩等级为 F")