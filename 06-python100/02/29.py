# 密码验证：检查密码长度是否大于8且包含数字和字母。

pwd = input("请输入密码：")

# len(pwd) > 8 检查密码长度是否大于8
# any(char.isdigit() for char in pwd) 

# 在 Python 中，any() 是一个非常强大且常用的内置函数。
# 它的核心作用是：检查可迭代对象（如列表、元组等）中，是否至少有一个元素为真（True）12。

# char.isdigit() 是字符串方法，用于检查字符串中的字符是否为数字字符。
# any(char.isdigit() for char in pwd) 这段代码的意思是：
# 对于密码字符串 pwd 中的每个字符 char，检查它是否是数字字符

# char.isalpha() 是字符串方法，用于检查字符串中的字符是否为字母字符。

if (len(pwd) > 8 and any(char.isdigit() for char in pwd) and any(char.isalpha() for char in pwd)):
    print("密码有效。")
else:
    print("密码无效。请确保密码长度大于8且包含数字和字母。")