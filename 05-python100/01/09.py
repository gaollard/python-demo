# 温度转换器：摄氏度与华氏度互相转换。

def celsius_to_fahrenheit(celsius):
    return (celsius * 1.8) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

print("20°C 转换为华氏度:", celsius_to_fahrenheit(20))      # 输出: 68.0
print("86°F 转换为摄氏度:", round(fahrenheit_to_celsius(86), 2)) # 输出: 30.0
