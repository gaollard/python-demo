import random

print("随机生成一个0-1之间的浮点数: ", random.random())
print("随机生成一个1-10之间的整数: ", random.randint(1, 10))
print("等价于从 range(1, 10, 2) → 1, 3, 5, 7, 9 里随机挑一个: ", random.randrange(1, 10, 2))

# 指定区间的浮点数 [a, b]
print("随机浮点数 [1.5, 3.5]: ", random.uniform(1.5, 3.5))

# 从序列中随机选一个 / 多个
fruits = ["apple", "banana", "cherry", "date"]
print("随机选一个: ", random.choice(fruits))
print("随机选 2 个(可重复): ", random.choices(fruits, k=2))
print("随机选 2 个(不重复): ", random.sample(fruits, k=2))

# 打乱原列表顺序（原地修改）
nums = [1, 2, 3, 4, 5]
random.shuffle(nums)
print("打乱后: ", nums)

# 固定种子后，结果可复现（调试常用）
random.seed(42)
print("seed=42 时的 randint: ", random.randint(1, 100))