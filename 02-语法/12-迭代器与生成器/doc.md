# 迭代器与生成器

Python 的 `for` 循环能遍历列表、字符串、字典等，靠的是**可迭代协议**。理解迭代器与生成器，就能写出更省内存、更清晰的惰性求值代码。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 可迭代对象（Iterable） | 实现了 `__iter__()`，能被 `for` / `iter()` 使用 | `list`、`str`、`dict`、`range`、文件对象 |
| 迭代器（Iterator） | 实现了 `__next__()`（及 `__iter__`），一次产出一个值 | `iter([1,2,3])`、生成器对象 |
| 生成器（Generator） | 用 `yield` 写出的特殊迭代器，按需产出 | `def g(): yield 1` |

关系可以记成：

```
可迭代对象 ──iter()──▶ 迭代器 ──next()──▶ 下一个值
                            ▲
生成器是迭代器的一种 ─────────┘
```

## 可迭代对象 vs 迭代器

```python
nums = [10, 20, 30]          # 可迭代对象（不是迭代器）
it = iter(nums)              # 得到迭代器

print(next(it))              # 10
print(next(it))              # 20
print(next(it))              # 30
# print(next(it))            # StopIteration：耗尽后继续取会抛异常

# 列表可以反复遍历；迭代器只能“走一遍”
for x in nums:
    print(x)
for x in nums:
    print(x)                 # 仍然可以

it2 = iter(nums)
print(list(it2))             # [10, 20, 30]
print(list(it2))             # []  —— 已经耗尽
```

判断方式：

```python
from collections.abc import Iterable, Iterator

print(isinstance([1, 2], Iterable))   # True
print(isinstance([1, 2], Iterator))   # False
print(isinstance(iter([1, 2]), Iterator))  # True
```

`for` 循环的本质大致是：

```python
# for x in obj: ...
it = iter(obj)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    # 循环体
```

## 自定义迭代器

实现 `__iter__` 和 `__next__`：

```python
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

for n in CountDown(3):
    print(n)                 # 3 2 1
```

可迭代对象也可以让 `__iter__` 返回一个新的迭代器，这样就能被多次 `for`：

```python
class RangeLike:
    def __init__(self, n: int):
        self.n = n

    def __iter__(self):
        return CountDown(self.n)   # 每次 for 都拿新迭代器
```

## 生成器函数（`yield`）

用 `yield` 比手写迭代器类简单得多：函数里一旦出现 `yield`，调用它不会立刻执行完，而是返回一个**生成器对象**。

```python
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
```

执行过程：

1. 调用 `count_down(3)` → 得到生成器，函数体尚未真正跑完
2. 每次 `next()` → 运行到下一个 `yield`，产出值并暂停
3. 再次 `next()` → 从暂停处继续
4. 函数结束（或 `return`）→ 抛出 `StopIteration`

```python
def gen():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = gen()
print(next(g))   # 打印 start，得到 1
print(next(g))   # 打印 middle，得到 2
# next(g)        # 打印 end，然后 StopIteration
```

## 生成器表达式

类似列表推导，但用圆括号，**惰性求值**，不一次性建完整列表：

```python
# 列表推导：立刻生成全部元素，占内存
squares_list = [x * x for x in range(5)]
print(squares_list)          # [0, 1, 4, 9, 16]

# 生成器表达式：按需产出
squares_gen = (x * x for x in range(5))
print(squares_gen)           # <generator object ...>
print(next(squares_gen))     # 0
print(list(squares_gen))     # [1, 4, 9, 16]

# 作为函数唯一参数时，可省略外层括号
total = sum(x * x for x in range(5))
print(total)                 # 30
```

| | 列表推导 | 生成器表达式 |
|---|---|---|
| 写法 | `[...]` | `(...)` |
| 求值 | 立即 | 惰性 |
| 内存 | 装下全部元素 | 几乎只占当前状态 |
| 可复用 | 可多次遍历 | 用完即尽 |
| 适合 | 需要多次使用、长度不大 | 大数据、管道式处理 |

## 惰性求值的价值

处理大文件或无限序列时，生成器几乎不占额外内存：

```python
def read_lines(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:           # 文件对象本身就是惰性的
            yield line.rstrip("\n")

# 不会把整个文件读进内存
# for line in read_lines("big.txt"):
#     process(line)
```

无限序列也可以安全表达（配合 `break` / `islice` 使用）：

```python
def naturals():
    n = 0
    while True:
        yield n
        n += 1

from itertools import islice
print(list(islice(naturals(), 5)))   # [0, 1, 2, 3, 4]
```

## `yield from`

把一个可迭代对象的产出“委托”出去，避免手写循环：

```python
def flatten(items):
    for item in items:
        if isinstance(item, list):
            yield from flatten(item)   # 等价于 for x in flatten(item): yield x
        else:
            yield item

print(list(flatten([1, [2, [3, 4], 5], 6])))
# [1, 2, 3, 4, 5, 6]
```

## 生成器的进阶方法（了解即可）

```python
def echo():
    while True:
        value = yield           # 既产出又接收
        print("收到:", value)

g = echo()
next(g)          # 先推进到第一个 yield
g.send("hello")  # 收到: hello
g.close()        # 关闭生成器
```

- `send(value)`：向生成器内部发送值（协程式用法的基础）
- `throw(exc)`：在暂停处注入异常
- `close()`：终止生成器

日常写业务代码时，用 `for` / `next` / `yield` / `yield from` 就够了。

## 常见内置与工具

```python
# enumerate / zip / map / filter 都返回迭代器
print(list(enumerate(["a", "b"])))     # [(0, 'a'), (1, 'b')]
print(list(zip([1, 2], ["x", "y"])))   # [(1, 'x'), (2, 'y')]
print(list(map(str.upper, "ab")))      # ['A', 'B']

# itertools：组合、切片、链式等
from itertools import chain, count, cycle, islice

print(list(chain([1, 2], [3, 4])))     # [1, 2, 3, 4]
print(list(islice(count(10), 3)))      # [10, 11, 12]
print(list(islice(cycle("AB"), 5)))    # ['A', 'B', 'A', 'B', 'A']
```

## 对比小结

| | 列表等容器 | 迭代器 | 生成器 |
|---|---|---|---|
| 是否可多次遍历 | 是 | 否（耗尽） | 否（耗尽） |
| 内存 | 保存全部元素 | 保存状态 | 保存状态 |
| 创建方式 | 字面量 / 构造 | `__iter__`/`__next__` 或 `iter()` | `yield` / 生成器表达式 |
| 典型场景 | 需要随机访问、反复用 | 统一遍历协议 | 惰性管道、大文件、无限流 |

## 实践建议

1. **能 `for` 就别手动 `next`**，除非确实要精细控制。
2. **大数据、流式处理优先生成器**，避免先 `list(...)` 再处理。
3. **需要多次遍历**：用列表，或每次重新调用生成器函数 / 重新 `iter(可迭代对象)`。
4. **自定义遍历逻辑**：优先写生成器函数，比手写迭代器类更短、更不容易错。
5. **注意耗尽**：`list(it)`、`for x in it` 之后，同一个迭代器/生成器就空了。
