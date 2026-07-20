# 门票价格：根据年龄和是否为学生，计算游乐园门票价格。

age = int(input("请输入年龄："))
is_student = input("是否为学生？(y/n)：").strip().lower() == 'y'

if age < 12:
    price = 10  # 儿童票
elif age < 18:
    price = 15  # 青少年票
elif age < 60:
    price = 20  # 成人票
else:
    price = 12  # 老年票


if is_student:
    price *= 0.8  # 学生票享受8折优惠

# .2f 格式化输出，保留两位小数

print(f"门票价格为: {price:.2f} 元")