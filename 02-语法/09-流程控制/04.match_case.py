# match / case 基本用法（需要 Python 3.10+）

status = 404

match status:
    case 200:
        print("成功")
    case 404:
        print("未找到")
    case 500:
        print("服务器错误")
    case _:
        print("未知状态码")

# 多值匹配（或模式）    
day = "Sat"

match day:
    case "Mon" | "Tue" | "Wed" | "Thu" | "Fri":
        print("工作日")
    case "Sat" | "Sun":
        print("周末")
    case _:
        print("无效日期")

# 捕获变量 + 元组结构匹配
point = (3, 5)

match point:
    case (0, 0):
        print("原点")
    case (x, 0):
        print(f"在 X 轴上，x = {x}")
    case (0, y):
        print(f"在 Y 轴上，y = {y}")
    case (x, y):
        print(f"点坐标: ({x}, {y})")

# 守卫条件
age = 20

match age:
    case n if n < 18:
        print("未成年")
    case n if 18 <= n < 65:
        print("成年人")
    case n if n >= 65:
        print("老年人")

# 序列匹配
command = ["go", "north"]

match command:
    case ["quit"]:
        print("退出")
    case ["go", direction]:
        print(f"向 {direction} 走")
    case ["drop", *items]:
        print(f"丢弃: {items}")
    case _:
        print("未知命令")

# 映射匹配
user = {"name": "Alice", "age": 20}

match user:
    case {"name": name, "age": age} if age >= 18:
        print(f"{name} 已成年")
    case {"name": name}:
        print(f"用户: {name}")
