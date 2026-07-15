# 年龄计算器：输入出生年份，计算并打印当前年龄。

from datetime import date

birth=int(input("请输入您的出生年份："))
current_year=date.today().year
age=current_year-birth
print("您的年龄为：",age)