#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 字符串常见操作示例

# 1. 字符串拼接
print("\n1. 字符串拼接")
str1 = "Hello"
str2 = "World"
print(str1 + " " + str2)  # 使用 + 运算符
print(" ".join([str1, str2]))  # 使用 join 方法

# 2. 字符串替换
print("\n2. 字符串替换")
original_str = "Hello World"
print(original_str.replace("World", "Python"))
print(original_str.replace("l", "x"))  # 替换所有匹配项
print(original_str.replace("l", "x", 1))  # 只替换第一个匹配项

# 3. 字符串查找
print("\n3. 字符串查找")
search_str = "Hello World"
print(search_str.find("World"))  # 返回第一次出现的索引
print(search_str.find("Python"))  # 未找到返回 -1
print(search_str.index("World"))  # 与 find 类似，但未找到会抛出异常

# 4. 字符串大小写转换
print("\n4. 字符串大小写转换")
mixed_case = "Hello World"
print(mixed_case.upper())  # 全部大写
print(mixed_case.lower())  # 全部小写
print(mixed_case.title())  # 首字母大写
print(mixed_case.capitalize())  # 第一个字符大写，其余小写

# 5. 字符串去除空白
print("\n5. 字符串去除空白")
whitespace_str = "   Hello World   "
print(whitespace_str.strip())  # 去除两端空白
print(whitespace_str.lstrip())  # 去除左端空白
print(whitespace_str.rstrip())  # 去除右端空白

# 6. 字符串格式化
print("\n6. 字符串格式化")
name = "Python"
age = 30
print("Hello, %s! You are %d years old." % (name, age))  # % 格式化
print("Hello, {}! You are {} years old.".format(name, age))  # format 方法
print("Hello, {}! You are {} years old.".format(name, age))  # 替代 f-string

# 7. 字符串长度
print("\n7. 字符串长度")
test_str = "Hello World"
print(len(test_str))

# 8. 字符串切片
print("\n8. 字符串切片")
slice_str = "Hello World"
print(slice_str[0])  # 第一个字符
print(slice_str[-1])  # 最后一个字符
print(slice_str[0:5])  # 从索引 0 到 4 的字符
print(slice_str[6:])  # 从索引 6 到末尾的字符
print(slice_str[:5])  # 从开头到索引 4 的字符
print(slice_str[::2])  # 步长为 2 的字符
print(slice_str[::-1])  # 反转字符串

# 9. 字符串判断
print("\n9. 字符串判断")
test_str = "Hello World"
print(test_str.startswith("Hello"))  # 是否以 "Hello" 开头
print(test_str.endswith("World"))  # 是否以 "World" 结尾
print(test_str.isalpha())  # 是否全为字母
print(test_str.isdigit())  # 是否全为数字
print(test_str.isalnum())  # 是否全为字母或数字
print(test_str.islower())  # 是否全为小写
print(test_str.isupper())  # 是否全为大写

# 10. 字符串统计
print("\n10. 字符串统计")
count_str = "Hello World"
print(count_str.count("l"))  # 统计 "l" 出现的次数
print(count_str.count("o"))  # 统计 "o" 出现的次数

# 11. 字符串分割（扩展）
print("\n11. 字符串分割")
split_str = "Hello,World,Python"
print(split_str.split(","))  # 按逗号分割
print(split_str.split(",", 1))  # 按逗号分割，只分割一次

# 12. 字符串连接
print("\n12. 字符串连接")
join_list = ["Hello", "World", "Python"]
print(", ".join(join_list))  # 用逗号和空格连接列表元素