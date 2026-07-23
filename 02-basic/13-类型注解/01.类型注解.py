a: int = 10
b: str = "10"
c: bool = True
d: float = 10.0
e: list[int] = [1, 2, 3]
f: tuple[int, str] = (1, "10")
g: dict[str, int] = {"a": 1, "b": 2}
h: set[int] = {1, 2, 3}
i: frozenset[int] = frozenset({1, 2, 3})
j: bytes = b"10"
k: bytearray = bytearray(b"10")
l: memoryview = memoryview(b"10")

# 类型注解只是提示，不会强制类型检查
a = "str"

print(a)
