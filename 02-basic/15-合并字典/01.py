dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# 合并（dict2 的值会覆盖 dict1 中相同的键）
merged = dict1 | dict2
print(merged)  # {'a': 1, 'b': 3, 'c': 4}

# print(dict1 + dict2) // error