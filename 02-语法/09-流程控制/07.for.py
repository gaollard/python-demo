student = {"姓名": "小明", "年龄": 18}

# 遍历键值对（最常用）
for key, value in student.items():
    print(f"{key}: {value}")

# 仅遍历键
for key in student:
    print(key)

# 仅遍历值
for value in student.values():
    print(value)

students = ["小明", "小红", "小刚"]

for student in students:
    print(student)