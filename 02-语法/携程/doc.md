# async / await

`async` / `await` 是 Python 的**协程**语法（3.5+），配合标准库 `asyncio` 做**并发 I/O**：在等待网络、磁盘、定时器时让出控制权，单线程里跑多个任务。适合高并发的 I/O 密集场景，不适合靠它「加速」CPU 密集计算。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 协程函数（coroutine function） | 用 `async def` 定义的函数 | `async def fetch(): ...` |
| 协程对象（coroutine） | 调用协程函数得到的对象，需被调度才会执行 | `coro = fetch()` |
| `await` | 等待一个可等待对象完成，并交出控制权 | `await asyncio.sleep(1)` |
| 事件循环（event loop） | 调度协程、处理 I/O 就绪的「调度器」 | `asyncio.run(main())` |
| Task | 把协程包装成可并发调度的任务 | `asyncio.create_task(coro)` |
| Future | 表示「将来某个结果」的底层对象 | Task 是 Future 的子类 |

关系可以记成：

```
async def f(): ...     →  协程函数
f()                    →  协程对象（还没跑）
asyncio.run / await    →  交给事件循环执行
create_task            →  并发调度多个协程
```

## 为什么需要 async / await

同步写法：一次只干一件事，等 I/O 时线程空转：

```python
import time

def fetch_sync(name: str) -> str:
    time.sleep(1)          # 模拟网络 I/O
    return f"data-{name}"

def main():
    a = fetch_sync("A")
    b = fetch_sync("B")
    print(a, b)            # 总共约 2 秒

main()
```

异步写法：等待时切换去做别的任务，总耗时接近最慢那个：

```python
import asyncio

async def fetch(name: str) -> str:
    await asyncio.sleep(1)  # 可等待的「假睡眠」，会让出控制权
    return f"data-{name}"

async def main():
    a, b = await asyncio.gather(fetch("A"), fetch("B"))
    print(a, b)             # 总共约 1 秒

asyncio.run(main())
```

要点：`await asyncio.sleep` 和 `time.sleep` 不一样——前者让出事件循环，后者会**堵死**整条循环。

## 基本用法

### 定义与运行

```python
import asyncio

async def hello(name: str) -> str:
    await asyncio.sleep(0.1)
    return f"hello, {name}"

async def main():
    msg = await hello("Ada")
    print(msg)              # hello, Ada

asyncio.run(main())         # 程序入口：创建并跑完事件循环
```

注意：

- `async def` 里才能用 `await`。
- 直接调用 `hello("Ada")` 只得到协程对象，**不会执行**；必须 `await` 或交给 `asyncio.run` / Task。
- 脚本入口通常用 `asyncio.run(main())`，不要自己手动 `get_event_loop().run_until_complete(...)`（除非兼容旧代码）。

### 可等待对象（Awaitable）

能写在 `await` 右边的东西：

1. **协程**：`await hello("Ada")`
2. **Task**：`await asyncio.create_task(hello("Ada"))`
3. **Future**：较低层，多数业务代码不直接碰

```python
import asyncio

async def work():
    return 42

async def main():
    # 1) 直接 await 协程：顺序执行
    print(await work())

    # 2) 先包装成 Task，再 await：可与其它任务交错
    t = asyncio.create_task(work())
    print(await t)

asyncio.run(main())
```

## 并发：Task 与 gather

### `create_task`：立刻开始调度

```python
import asyncio
import time

async def job(n: int) -> int:
    await asyncio.sleep(1)
    return n * n

async def main():
    t0 = time.perf_counter()
    t1 = asyncio.create_task(job(3))
    t2 = asyncio.create_task(job(4))
    # 两个 Task 已经在跑；这里可以干别的事
    r1, r2 = await t1, await t2
    print(r1, r2)                           # 9 16
    print(f"{time.perf_counter() - t0:.1f}s")  # ~1.0s

asyncio.run(main())
```

### `asyncio.gather`：一批一起等

```python
import asyncio

async def job(n: int) -> int:
    await asyncio.sleep(0.5)
    return n

async def main():
    results = await asyncio.gather(job(1), job(2), job(3))
    print(results)          # [1, 2, 3]，顺序与入参一致

asyncio.run(main())
```

`gather` 默认：其中一个抛错会立刻把异常抛给调用方，其它任务仍可能继续跑。需要「收齐所有结果（含异常）」时：

```python
results = await asyncio.gather(job(1), job(2), return_exceptions=True)
# 元素要么是返回值，要么是 Exception 实例
```

### `asyncio.TaskGroup`（3.11+）：结构化并发

更推荐的写法：一组任务同生共死，任一失败会取消同组其它任务并抛出异常组。

```python
import asyncio

async def job(n: int) -> int:
    await asyncio.sleep(0.2)
    if n == 2:
        raise ValueError("boom")
    return n

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(job(1))
            t2 = tg.create_task(job(2))
            t3 = tg.create_task(job(3))
        # 走出 with 时全部成功才会到这里
    except* ValueError as eg:
        print("failed:", eg.exceptions)

    # 若全部成功，可用 t1.result() 等取结果

asyncio.run(main())
```

## 超时、取消与保护

### 超时

```python
import asyncio

async def slow():
    await asyncio.sleep(5)
    return "done"

async def main():
    try:
        result = await asyncio.wait_for(slow(), timeout=1.0)
    except TimeoutError:          # 3.11+；更早是 asyncio.TimeoutError（同是 TimeoutError 别名）
        print("超时了")
    else:
        print(result)

asyncio.run(main())
```

### 取消

```python
import asyncio

async def worker():
    try:
        while True:
            print("working")
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("被取消，做清理")
        raise                     # 通常应重新抛出，让取消真正生效

async def main():
    t = asyncio.create_task(worker())
    await asyncio.sleep(1.2)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("main 确认任务已取消")

asyncio.run(main())
```

### `asyncio.shield`：挡住一层取消

外层 `wait_for` 超时取消时，不希望内层协程一起被取消，可用 `shield`（仍要自己处理后续结果）：

```python
import asyncio

async def important():
    await asyncio.sleep(2)
    return "ok"

async def main():
    try:
        await asyncio.wait_for(asyncio.shield(important()), timeout=0.5)
    except TimeoutError:
        print("外层超时；内层可能仍在跑")

asyncio.run(main())
```

## 异步上下文管理器与异步迭代

### `async with`

需要异步获取/释放资源时用：

```python
import asyncio

class AsyncConn:
    async def __aenter__(self):
        await asyncio.sleep(0.05)
        print("open")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0.05)
        print("close")
        return False

    async def query(self):
        return 1

async def main():
    async with AsyncConn() as conn:
        print(await conn.query())

asyncio.run(main())
```

### `async for`

异步可迭代对象实现 `__aiter__` / `__anext__`：

```python
import asyncio

class AsyncCounter:
    def __init__(self, n: int):
        self.n = n
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        await asyncio.sleep(0.05)
        self.i += 1
        return self.i

async def main():
    async for x in AsyncCounter(3):
        print(x)                # 1 2 3

asyncio.run(main())
```

生成器也有异步版：`async def` + `yield` 得到异步生成器，用 `async for` 消费。

## 和线程 / 进程怎么配合

事件循环里**不要**跑长时间 CPU 计算或阻塞式调用，否则卡住所有协程。常见做法：

```python
import asyncio
import time

def blocking_io():
    time.sleep(1)               # 阻塞型库
    return "from-thread"

async def main():
    # 丢到默认线程池，避免堵事件循环
    result = await asyncio.to_thread(blocking_io)
    print(result)

asyncio.run(main())
```

| 场景 | 做法 |
|---|---|
| 大量网络/文件等待 | `async`/`await` + asyncio |
| 阻塞型第三方库 | `asyncio.to_thread` 或自行用 `run_in_executor` |
| CPU 密集（算力） | `multiprocessing` / `ProcessPoolExecutor`，别指望协程加速 |

## 常见坑

1. **忘了 await**  
   `hello()` 只创建协程，还会触发 `RuntimeWarning: coroutine was never awaited`。

2. **在协程里用 `time.sleep` / 同步 `requests`**  
   会阻塞事件循环，并发立刻失效。改用 `asyncio.sleep`、`httpx`/`aiohttp` 等异步库，或 `to_thread`。

3. **在普通函数里写 `await`**  
   语法错误。要么把函数改成 `async def`，要么用 `asyncio.run` 包一层入口。

4. **并发了但仍然串行**  
   `await f(); await g()` 是顺序的；要并发需先 `create_task` / `gather` / `TaskGroup`。

5. **从同步代码「半路」调协程**  
   已在跑的循环里不要再 `asyncio.run`；用 `create_task`，或 `asyncio.get_running_loop()`。嵌套 `run` 会报错。

6. **取消后吞掉 `CancelledError`**  
   清理可以做，但通常要 `raise`，否则任务看起来「取消不掉」。

## 对比小结

| | 同步顺序 | 多线程 | async/await |
|---|---|---|---|
| 切换代价 | 无 | 线程切换，偏重 | 协程切换，很轻 |
| 适合 | 逻辑简单、I/O 少 | 阻塞库、少量并行 | 高并发 I/O |
| 并行 CPU | 受 GIL 限 | 受 GIL 限 | 不提供 CPU 并行 |
| 代码模型 | 直观 | 锁/共享状态 | 单线程协作，少锁 |
| 典型入口 | 直接调用 | `Thread` | `asyncio.run` |

## 实践建议

1. **入口只用一处 `asyncio.run(main())`**，其余层层 `await`。
2. **并发用 `TaskGroup`（3.11+）或 `gather`**，避免手写一堆裸 Task 却忘记 await。
3. **I/O 一律可等待**：`asyncio.sleep`、异步 HTTP/DB 驱动；阻塞调用丢进 `to_thread`。
4. **设超时**：对外请求用 `asyncio.wait_for` 或 API 自带 timeout，避免任务挂死。
5. **取消要可清理**：用 `try/finally` 或 `async with` 释放资源；慎吞 `CancelledError`。
6. **先分清瓶颈**：I/O 密集 → asyncio；CPU 密集 → 多进程；阻塞库暂不可换 → 线程池。
