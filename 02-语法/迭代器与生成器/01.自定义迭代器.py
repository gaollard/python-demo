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

for n in val: # 3 2 1
    print(n)

for n in val:
    print(n)  # 不能：迭代器已耗尽，__iter__ 返回自身，不会有任何输出
