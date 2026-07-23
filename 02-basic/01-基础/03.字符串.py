name = "ada lovelace"

# 首字母大写
print(name.title())

# 全部大写

name = "Ada Lovelace"
print(name.upper())

# 全部小写
print(name.lower())

# 拼接字符串
first_name = "hello "
last_name = "world"
full_name = first_name + " " + last_name
print(full_name)

# 换行
print("Languages:\nPython\nC\nJavaScript")

# 制表符

print("\tPython")
    
# Python能够找出字符串开头和末尾多余的空白。要确保字符串末尾没有空白，可使用方法rstrip()。
favorite_language = ' python '
print('python')
print("hello"+favorite_language.rstrip() + "!")
print("hello"+favorite_language.lstrip() + "!")
print("hello"+favorite_language.strip() + "!")
