# 可迭代对象的 __iter__ 每次返回新的迭代器，因此可以被多次 for

class CountDown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


class RangeLike:
    def __init__(self, n: int):
        self.n = n

    def __iter__(self):
        return CountDown(self.n)   # 每次 for 都拿新迭代器


nums = RangeLike(3)

print("--- 第一次遍历 ---")
for n in nums:
    print(n)                       # 3 2 1

print("--- 第二次遍历 ---")
for n in nums:
    print(n)                       # 仍可输出 3 2 1
