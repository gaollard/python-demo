import time
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

# time 模块：本地时区信息（相对 UTC 的偏移，单位：秒）
print("UTC 偏移秒数 timezone:", time.timezone)  # 西半球为正，东八区通常是 -28800
print("夏令时偏移 altzone:", time.altzone)
print("是否实行夏令时 daylight:", time.daylight)
print("时区名称 tzname:", time.tzname)

# 本地时间 vs UTC
print("本地时间 localtime:", time.localtime())
print("UTC 时间 gmtime:", time.gmtime())

# datetime：带时区的时间（aware）vs 不带时区（naive）
now_naive = datetime.now()
now_utc = datetime.now(timezone.utc)
now_cn = datetime.now(timezone(timedelta(hours=8)))  # 固定 UTC+8
print("naive 本地时间:", now_naive)
print("UTC 时间:", now_utc)
print("UTC+8 时间:", now_cn)

# zoneinfo：按地区名取时区（推荐，会处理夏令时）
shanghai = datetime.now(ZoneInfo("Asia/Shanghai"))
tokyo = datetime.now(ZoneInfo("Asia/Tokyo"))
new_york = datetime.now(ZoneInfo("America/New_York"))
print("上海:", shanghai)
print("东京:", tokyo)
print("纽约:", new_york)

# 时区转换
utc_time = datetime.now(timezone.utc)
shanghai_time = utc_time.astimezone(ZoneInfo("Asia/Shanghai"))
print("UTC -> 上海:", shanghai_time)
