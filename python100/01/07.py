# 简单计算器：输入两个数和运算符，打印计算结果。

num1=input("请输入第一个数字：")
num2=input("请输入第二个数字：")
operator=input("请输入运算符：")

result=0

if operator=="+":
    result=int(num1)+int(num2)
elif operator=="-":
    result=int(num1)-int(num2)
elif operator=="*":
    result=int(num1)*int(num2)
elif operator=="/":
    result=int(num1)/int(num2)

print("计算结果为：",result)
