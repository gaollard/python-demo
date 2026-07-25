# 上下文管理器

`with` 语句保证一段代码**进入时准备资源、离开时清理资源**，即使中途抛异常也会执行清理。文件、锁、数据库连接等场景几乎都会用到它。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 上下文管理器（Context Manager） | 实现了 `__enter__` / `__exit__` 的对象 | 文件对象、`threading.Lock()` |
| `with` 语句 | 自动调用进入/退出协议的语法糖 | `with open(...) as f:` |
| 上下文变量 | `__enter__` 的返回值，可用 `as` 绑定 | `as f` 里的 `f` |

关系可以记成：

```
with 表达式 as 变量:
    代码块
        │
        ▼
调用 __enter__() ──▶ 返回值赋给 as 变量
        │
        ▼
执行 with 代码块
        │
        ▼
无论成功/异常，都调用 __exit__(...)
```

## 为什么需要 `with`

不用 `with` 时，容易忘记关闭，或异常路径漏清理：

```python
f = open("demo.txt", "w", encoding="utf-8")
try:
    f.write("hello")
finally:
    f.close()   # 必须自己保证清理
```

等价且更清晰的写法：

```python
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("hello")
# 离开 with 块后，文件一定会被关闭
```

## `with` 的执行流程

```python
class DemoCM:
    def __enter__(self):
        print("enter")
        return "资源对象"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit", exc_type)
        return False   # False / None：不吞掉异常；True：抑制异常

with DemoCM() as value:
    print("body:", value)
# 输出：
# enter
# body: 资源对象
# exit None
```

发生异常时：

```python
with DemoCM() as value:
    print("before error")
    raise ValueError("boom")
# 输出：
# enter
# before error
# exit <class 'ValueError'>
# 然后异常继续向外抛出（因为 __exit__ 返回了 False）
```

`__exit__` 的三个参数：

| 参数 | 含义 |
|---|---|
| `exc_type` | 异常类型；无异常时为 `None` |
| `exc_val` | 异常实例；无异常时为 `None` |
| `exc_tb` |  traceback；无异常时为 `None` |

返回值约定：

- 返回 `False` / `None`：异常继续传播（默认行为）
- 返回 `True`：抑制异常，`with` 之后的代码继续执行

## 自定义上下文管理器（类）

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"耗时: {self.elapsed:.6f}s")
        return False

with Timer() as t:
    sum(range(1_000_000))
print("记录的耗时:", t.elapsed)
```

再看一个“自动加解锁”的例子：

```python
import threading

class Locked:
    def __init__(self, lock: threading.Lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()
        return self.lock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        return False

lock = threading.Lock()
with Locked(lock):
    # 临界区
    pass
```

实际项目里通常直接写 `with lock:`，因为 `threading.Lock` 本身就是上下文管理器。

## `contextlib.contextmanager`（生成器写法）

很多场景不必手写类，用装饰器把生成器变成上下文管理器更短：

```python
from contextlib import contextmanager

@contextmanager
def open_and_count(path: str):
    f = open(path, "w", encoding="utf-8")
    try:
        yield f          # yield 之前 = __enter__；之后 = __exit__
    finally:
        f.close()
        print("已关闭")

with open_and_count("demo.txt") as f:
    f.write("hi")
```

结构约定：

1. `yield` 之前：准备资源（对应 `__enter__`）
2. `yield` 的值：给 `as` 绑定
3. `yield` 之后 / `finally`：清理资源（对应 `__exit__`）

带异常处理时：

```python
from contextlib import contextmanager

@contextmanager
def suppress_value_error():
    try:
        yield
    except ValueError as e:
        print("吞掉 ValueError:", e)

with suppress_value_error():
    raise ValueError("忽略我")
print("继续执行")
```

## 多个上下文管理器

可以写在同一行，按从左到右进入，按相反顺序退出：

```python
with open("a.txt", "w", encoding="utf-8") as fa, open("b.txt", "w", encoding="utf-8") as fb:
    fa.write("A")
    fb.write("B")
```

嵌套写法效果相同，但更啰嗦：

```python
with open("a.txt", "w", encoding="utf-8") as fa:
    with open("b.txt", "w", encoding="utf-8") as fb:
        fa.write("A")
        fb.write("B")
```

Python 3.10+ 也支持括号换行：

```python
with (
    open("a.txt", "w", encoding="utf-8") as fa,
    open("b.txt", "w", encoding="utf-8") as fb,
):
    fa.write("A")
    fb.write("B")
```

## 常见内置与标准库用法

```python
# 文件
with open("demo.txt", encoding="utf-8") as f:
    data = f.read()

# 线程锁
import threading
lock = threading.Lock()
with lock:
    pass

# 临时改当前目录
from contextlib import chdir
from pathlib import Path

with chdir(Path("/tmp")):
    print(Path.cwd())

# 重定向标准输出
import io
from contextlib import redirect_stdout

buf = io.StringIO()
with redirect_stdout(buf):
    print("hello")
print("捕获到:", buf.getvalue())   # hello\n

# 忽略指定异常
from contextlib import suppress

with suppress(FileNotFoundError):
    open("不存在.txt").close()
```

`ExitStack`：动态管理数量不固定的上下文：

```python
from contextlib import ExitStack

paths = ["a.txt", "b.txt", "c.txt"]
with ExitStack() as stack:
    files = [stack.enter_context(open(p, "w", encoding="utf-8")) for p in paths]
    for f in files:
        f.write("ok")
# 离开时按进入的反序全部关闭
```

## `async with`（异步上下文管理器）

异步代码里用 `__aenter__` / `__aexit__`：

```python
class AsyncCM:
    async def __aenter__(self):
        print("aenter")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("aexit")
        return False

# 在 async 函数中：
# async with AsyncCM() as cm:
#     ...
```

也可用 `@asynccontextmanager`：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_resource():
    print("准备")
    try:
        yield "资源"
    finally:
        print("清理")

# async with async_resource() as r:
#     print(r)
```

## 对比小结

| | `try/finally` | 类实现上下文管理器 | `@contextmanager` |
|---|---|---|---|
| 可读性 | 一般 | 适合有状态/可复用对象 | 短逻辑最清晰 |
| 复用性 | 差（散落各处） | 强 | 强 |
| 异常策略 | 手写 | `__exit__` 返回值控制 | `try/except` 包住 `yield` |
| 典型场景 | 一次性清理 | 锁、连接池、计时器 | 文件包装、临时配置 |

## 实践建议

1. **有获取就有释放**：文件、套接字、锁、事务，优先 `with`，少写裸 `open` + 手动 `close`。
2. **短逻辑用 `@contextmanager`**，有复杂状态或多个方法时再写成类。
3. **清理放 `finally` / `__exit__`**：保证异常路径也会执行。
4. **默认不要吞异常**：`__exit__` 返回 `True` 要有明确理由。
5. **数量不固定时用 `ExitStack`**，避免手写多层嵌套 `with`。
6. **异步代码用 `async with`**，不要把同步上下文管理器直接套进协程里当“异步清理”。
