# 闰年判断：判断输入的年份是否为闰年。
# 闰年的判断规则：
# 1. 能被4整除且不能被100整除的年份是闰年
# 2. 能被400整除的年份是闰年

year=int(input("Enter a year: "))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")