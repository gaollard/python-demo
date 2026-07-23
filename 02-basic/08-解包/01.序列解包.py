# 列表/元组解包
coordinates = [10, 20]
x, y = coordinates
print(x, y)  # 输出: 10 20

# 字符串解包
a, b, c = "ABC"
print(a, b, c)  # 输出: A B C

# 字典解包（默认解包键）
data = {"name": "Alice", "age": 25}
key1, key2 = data
print(key1, key2)  # 输出: name age

# 收集剩余元素
numbers = [1, 2, 3, 4, 5]
first, *middle, last = numbers
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5

# 仅获取首尾
head, *tail = [10, 20, 30, 40]
print(head)  # 10
print(tail)  # [20, 30, 40]


# 仅获取最后一个
*head, tail = [10, 20, 30, 40]
print(head)  # [10, 20, 30]
print(tail)  # 40


# 使用 .items() 方法可以同时解包键和值，这在遍历字典时比手动索引优雅得多。
user = {"name": "Bob", "score": 95}
for key, value in user.items():
    print(f"{key}: {value}")
