class CountDown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self          # 迭代器的 __iter__ 通常返回自身

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

val = CountDown(3)

print(next(val)) # 3
print(next(val)) # 2
print(next(val)) # 1
print(next(val)) # 报错 StopIteration