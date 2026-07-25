def count_down(n: int):
    while n > 0:
        yield n
        n -= 1

g = count_down(3)
print(g)                     # <generator object count_down at ...>
print(next(g))               # 3
print(next(g))               # 2
print(list(count_down(3)))   # [3, 2, 1]

for x in count_down(3):
    print(x)