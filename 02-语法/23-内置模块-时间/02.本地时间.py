import time

print("时间戳: ", time.time()) # 单位: 秒
print("本地时间: ", time.localtime())
print("本地时间: ", time.localtime().tm_year)
print("本地时间: ", time.localtime().tm_mon)
print("本地时间: ", time.localtime().tm_mday)
print("本地时间: ", time.localtime().tm_hour)
print("本地时间: ", time.localtime().tm_min)
print("本地时间: ", time.localtime().tm_sec)
print("本地时间: ", time.localtime().tm_wday)
print("本地时间: ", time.localtime().tm_yday)

# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# print(time.strptime("2026-07-25 10:00:00", "%Y-%m-%d %H:%M:%S"))
# print(time.mktime(time.strptime("2026-07-25 10:00:00", "%Y-%m-%d %H:%M:%S")))
# print(time.ctime())
# print(time.asctime())
# print(time.gmtime())
# print(time.localtime())
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# print(time.strptime("2026-07-25 10:00:00", "%Y-%m-%d %H:%M:%S"))