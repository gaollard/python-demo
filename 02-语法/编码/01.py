# str（文本） <-> bytes（字节）靠编码转换

text = "你好 Python"
print("1", type(text))          # <class 'str'>

# encode：字符串 → 字节（默认 utf-8）
data = text.encode("utf-8")
print("2", data)                # b'\xe4\xbd\xa0\xe5\xa5\xbd Python'
print("3",type(data))          # <class 'bytes'>
print("4", list(data[:6]))      # [228, 189, 160, 229, 165, 189]  每个中文占 3 字节

# decode：字节 → 字符串
print("5", data.decode("utf-8"))  # 你好 Python

# 编码不一致会报错或乱码
gbk = text.encode("gbk")
print("6", gbk)                 # 与 utf-8 字节不同
# print(gbk.decode("utf-8"))  # UnicodeDecodeError
print("7", gbk.decode("gbk"))   # 你好 Python

print("8", data[:6].decode("utf-8", errors="ignore"))   # 你好


# 字符串转 base64
import base64

base64_data = base64.b64encode(data)
print("9", base64_data)

# base64 转字符串
print("10", base64.b64decode(base64_data).decode("utf-8"))