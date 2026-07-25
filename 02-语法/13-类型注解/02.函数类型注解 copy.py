def calc(a: int, b: int) -> int:
    return a + b

# print(calc(1, 2))
# print(calc(1, "3")) # 会报错 TypeError: unsupported operand type(s) for +: 'int' and 'str'


def calc2(scores: list[int]) -> int:
    return sum(scores)

# print(calc2([4, 3]))
# print(calc2([2, "2"])) # TypeError: unsupported operand type(s) for +: 'int' and 'str'

def calc3(scores: list[int]) -> tuple[int, float, int]:
    return sum(scores), sum(scores) / len(scores), max(scores)

# print(calc3([4, 3])) # (7, 3.5, 4)

