import re

# 匹配字符串中的数字
text = "订单号: 12345, 金额: 99.5"
match = re.search(r'\d+', text)

if match:
    print("找到数字:", match.group())