sts = dict(name='张三', age=18)

print(sts.keys())
print(sts.values())
print(sts.items())

for key, value in sts.items():
    print(key, value)

for key in sts.keys():
    print(key)

for value in sts.values():
    print(value)