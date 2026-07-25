import time

# 格式化时间
print("time.strftime: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

# 解析时间
print("time.strptime: ", time.strptime("2026-07-25 10:00:00", "%Y-%m-%d %H:%M:%S"))

# 转换为时间戳
print("time.mktime: ", time.mktime(time.strptime("2026-07-25 10:00:00", "%Y-%m-%d %H:%M:%S")))

# 转换为时间字符串
print(time.ctime()) # 本地时间
print(time.asctime()) # 本地时间
print(time.gmtime()) # 格林尼治时间