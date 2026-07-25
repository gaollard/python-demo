import re

text = "apple123 banana456 cherry789"

# findall: 只返回匹配的字符串列表
print(re.findall(r'\d+', text))  # ['123', '456', '789']

# finditer: 返回Match对象迭代器，可获取位置信息
for match in re.finditer(r'\d+', text):
    print(f"匹配内容: {match.group()}, 位置: {match.span()}")
# 匹配内容: 123, 位置: (5, 8)
# 匹配内容: 456, 位置: (15, 18)
# 匹配内容: 789, 位置: (26, 29)