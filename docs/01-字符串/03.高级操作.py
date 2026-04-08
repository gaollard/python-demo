#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 字符串高级操作示例

# 1. 字符串填充
print("\n1. 字符串填充")
filler_str = "Python"
print(filler_str.ljust(10))  # 左对齐，右侧填充空格
print(filler_str.rjust(10))  # 右对齐，左侧填充空格
print(filler_str.center(10))  # 居中，两侧填充空格
print(filler_str.ljust(10, "*"))  # 左对齐，右侧填充 *
print(filler_str.rjust(10, "*"))  # 右对齐，左侧填充 *
print(filler_str.center(10, "*"))  # 居中，两侧填充 *

# 2. 字符串编码和解码
print("\n2. 字符串编码和解码")
try:
    encode_str = "你好 Python"
    encoded = encode_str.encode("utf-8")  # 编码为 UTF-8
    print(encoded)
    decoded = encoded.decode("utf-8")  # 解码为字符串
    print(decoded)
except UnicodeDecodeError:
    print("编码解码操作在当前 Python 版本中可能有兼容性问题")

# 3. 字符串高级替换
print("\n3. 字符串高级替换")
try:
    import string
    trans_str = "Hello World"
    trans_table = string.maketrans("aeiou", "12345")  # 创建转换表
    print(trans_str.translate(trans_table))  # 使用转换表替换字符
except AttributeError:
    print("字符串转换操作在当前 Python 版本中可能有兼容性问题")

# 4. 字符串检查
print("\n4. 字符串检查")
check_str = "   Hello World   "
print(check_str.isspace())  # 是否全为空白字符
print("Hello".isspace())  # 是否全为空白字符
print("123".isdigit())  # 是否全为数字
print("abc123".isalnum())  # 是否全为字母或数字
print("abc".isalpha())  # 是否全为字母
print("ABC".isupper())  # 是否全为大写
print("abc".islower())  # 是否全为小写
print("Hello World".istitle())  # 是否为标题格式

# 5. 字符串分割和连接的高级用法
print("\n5. 字符串分割和连接的高级用法")
advanced_str = "Hello   World   Python"
print(advanced_str.split())  # 默认分割，处理多个空格
print(advanced_str.split(" "))  # 按单个空格分割

# 6. 字符串的startswith和endswith的高级用法
print("\n6. 字符串的startswith和endswith的高级用法")
startend_str = "Hello World.py"
print(startend_str.startswith(("Hello", "Hi")))  # 检查是否以多个前缀之一开头
print(startend_str.endswith((".py", ".txt")))  # 检查是否以多个后缀之一结尾

# 7. 字符串的格式化高级用法
print("\n7. 字符串的格式化高级用法")
format_str = "Hello {name}! You are {age} years old."
print(format_str.format(name="Python", age=30))  # 使用命名参数

# 8. 字符串的计数和查找高级用法
print("\n8. 字符串的计数和查找高级用法")
count_find_str = "Hello World Hello"
print(count_find_str.count("Hello"))  # 统计出现次数
print(count_find_str.find("Hello", 1))  # 从索引 1 开始查找
print(count_find_str.rfind("Hello"))  # 从右侧开始查找

# 9. 字符串的大小写转换高级用法
print("\n9. 字符串的大小写转换高级用法")
case_str = "Hello World"
print(case_str.swapcase())  # 大小写互换

# 10. 字符串的判断高级用法
print("\n10. 字符串的判断高级用法")
print(" ".isspace())  # 是否为空白字符
print("\t".isspace())  # 是否为空白字符
print("\n".isspace())  # 是否为空白字符
try:
    print("Hello".isprintable())  # 是否为可打印字符
    print("Hello\n".isprintable())  # 是否为可打印字符
except AttributeError:
    print("isprintable() 方法在当前 Python 版本中可能有兼容性问题")

# 11. 字符串的切片高级用法
print("\n11. 字符串的切片高级用法")
slice_adv_str = "Hello World Python"
print(slice_adv_str[::3])  # 步长为 3
print(slice_adv_str[::-2])  # 步长为 -2，反转字符串

# 12. 字符串的连接高级用法
print("\n12. 字符串的连接高级用法")
join_adv_list = ["Hello", "World", "Python"]
print("-".join(join_adv_list))  # 用连字符连接
print("\n".join(join_adv_list))  # 用换行符连接