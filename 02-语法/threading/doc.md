# threading

`threading` 是 Python 标准库的**多线程**模块。一个进程里可以跑多条执行流，适合把**阻塞 I/O**（网络、磁盘、数据库）重叠起来，提高吞吐。注意：在默认的 CPython 里有 **GIL**，多线程**不能**真正并行跑纯 Python 的 CPU 密集计算。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 线程（Thread） | 进程内的一条执行流，共享内存 | `threading.Thread(target=f)` |
| 主线程 | 启动进程时就有的那条线程 | `threading.main_thread()` |
| `start` / `join` | 启动线程；等待线程结束 | `t.start(); t.join()` |
| 守护线程（daemon） | 主线程退出时会被一并结束 | `Thread(..., daemon=True)` |
| 锁（Lock） | 互斥，保护共享可变状态 | `with lock:` |
| 队列（Queue） | 线程安全的任务/结果通道 | `queue.Queue` |
| GIL | 同一时刻通常只有一个线程在执行 Python 字节码 | I/O 时会释放 |

关系可以记成：

```
主线程
  │
  ├─ Thread(target=...).start()  →  后台跑函数
  ├─ join()                      →  等它结束
  └─ 共享内存 + Lock / Queue     →  协调读写，避免竞态
```

## 为什么需要 threading

单线程：等 I/O 时整条程序卡住。

```python
import time

def fetch(name: str) -> str:
    time.sleep(1)              # 模拟网络 / 磁盘等待
    return f"data-{name}"

def main():
    a = fetch("A")
    b = fetch("B")
    print(a, b)                # 总共约 2 秒

main()
```

多线程：等待时另一条线程可以继续干活，总耗时接近最慢那个：

```python
import threading
import time

def fetch(name: str, out: list[str]) -> None:
    time.sleep(1)
    out.append(f"data-{name}")

def main():
    out: list[str] = []
    t1 = threading.Thread(target=fetch, args=("A", out))
    t2 = threading.Thread(target=fetch, args=("B", out))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(out)                 # 顺序不定；总共约 1 秒

main()
```

要点：线程适合**阻塞库**（同步 `requests`、同步 DB 驱动等）；高并发纯 I/O 更优先考虑 `asyncio`（见 `携程/doc.md`）。

## 基本用法

### 创建与启动

```python
import threading
import time

def worker(n: int) -> None:
    print(f"start {n}")
    time.sleep(0.5)
    print(f"end {n}")

t = threading.Thread(target=worker, args=(1,), name="worker-1")
t.start()                      # 真正开始跑；不要对同一 Thread 调两次 start
t.join()                       # 阻塞到该线程结束
print("done", t.name)
```

用类继承也可以（少见，但旧代码常见）：

```python
import threading

class Worker(threading.Thread):
    def __init__(self, n: int):
        super().__init__()
        self.n = n

    def run(self) -> None:     # start() 会调用 run()
        print("work", self.n)

Worker(1).start()
```

日常更推荐 `target=` 函数，而不是子类化。

### 传参与取结果

`Thread` 本身**不返回** `target` 的返回值。常见做法：

1. 用可变容器 / 字典收集  
2. 用 `queue.Queue`  
3. 用 `concurrent.futures.ThreadPoolExecutor`（最省事）

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def job(n: int) -> int:
    return n * n

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = [pool.submit(job, i) for i in range(5)]
    for f in as_completed(futures):
        print(f.result())      # 0 1 4 9 16（完成顺序不定）
```

`map` 写法（按入参顺序拿结果）：

```python
from concurrent.futures import ThreadPoolExecutor

def job(n: int) -> int:
    return n * n

with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(job, range(5))))  # [0, 1, 4, 9, 16]
```

### 守护线程（daemon）

```python
import threading
import time

def background() -> None:
    while True:
        print("tick")
        time.sleep(1)

t = threading.Thread(target=background, daemon=True)
t.start()
time.sleep(2.5)
# 主线程结束 → 进程退出 → daemon 线程被直接掐掉，不一定有清理机会
```

规则：

- `daemon=True`：主线程（及所有非 daemon 线程）结束后，进程可退出，daemon 跟着没。
- 需要可靠收尾（写文件、关连接）时，**不要**只靠 daemon；用 `join`、事件通知，或在 `try/finally` 里清理。

### 当前线程与枚举

```python
import threading

print(threading.current_thread().name)
print(threading.main_thread().name)
print(threading.active_count())
for t in threading.enumerate():
    print(t.name, t.is_alive())
```

## 同步原语

多线程共享内存，读写同一可变对象时需要同步，否则会有**竞态条件**。

### `Lock`：互斥锁

```python
import threading

counter = 0
lock = threading.Lock()

def bump() -> None:
    global counter
    for _ in range(100_000):
        with lock:             # 等价于 acquire / release，异常也会释放
            counter += 1

threads = [threading.Thread(target=bump) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)                 # 400000；去掉 lock 往往对不上
```

- `RLock`：同一线程可重入加锁（递归调用同一把锁时用）。
- 持锁时间尽量短；不要在持锁时做慢 I/O。

### `Event`：一次性/可重置的信号

```python
import threading
import time

ready = threading.Event()

def waiter() -> None:
    print("waiting...")
    ready.wait()               # 阻塞到 set()
    print("go!")

threading.Thread(target=waiter).start()
time.sleep(1)
ready.set()                    # 唤醒所有在 wait 的线程
# ready.clear()                # 需要再次等待时清掉
```

### `Condition`：等条件再继续

```python
import threading

items: list[int] = []
cond = threading.Condition()

def consumer() -> None:
    with cond:
        while not items:       # 必须用 while，防止虚假唤醒
            cond.wait()
        print("got", items.pop(0))

def producer() -> None:
    with cond:
        items.append(42)
        cond.notify()          # 或 notify_all()

threading.Thread(target=consumer).start()
threading.Thread(target=producer).start()
```

### `Semaphore`：限制并发数

```python
import threading
import time

sem = threading.Semaphore(2)   # 最多 2 个线程同时进入

def access(n: int) -> None:
    with sem:
        print("in", n)
        time.sleep(0.5)
        print("out", n)

for i in range(5):
    threading.Thread(target=access, args=(i,)).start()
```

### `queue.Queue`：线程间传数据（优先推荐）

比到处加锁改共享 list 更稳：生产者 / 消费者通过队列解耦。

```python
import queue
import threading
import time

q: queue.Queue[str | None] = queue.Queue()

def producer() -> None:
    for i in range(3):
        q.put(f"item-{i}")
        time.sleep(0.1)
    q.put(None)                # 结束哨兵

def consumer() -> None:
    while True:
        item = q.get()
        try:
            if item is None:
                break
            print("consume", item)
        finally:
            q.task_done()

threading.Thread(target=producer).start()
threading.Thread(target=consumer).start()
q.join()                       # 等所有 task_done
```

常用变体：`LifoQueue`（栈）、`PriorityQueue`（优先级）。

## GIL 是什么

CPython 的 **GIL（Global Interpreter Lock）** 保证：同一时刻通常只有一个线程在执行 Python 字节码。

| 任务类型 | 多线程效果 |
|---|---|
| I/O 密集（等网络/磁盘） | 等待时会释放 GIL，其它线程能跑 → **有用** |
| CPU 密集（纯 Python 计算） | 线程抢 GIL，难加速，有时更慢 → **别指望** |
| 调用会释放 GIL 的 C 扩展（部分 numpy 等） | 可能在扩展内并行 → 视库而定 |

因此：

- **I/O 并发**：`threading` 或 `asyncio`
- **CPU 并行**：`multiprocessing` / `ProcessPoolExecutor`（多进程，绕过 GIL）
- Python 3.13+ 有可选的 free-threaded 构建（无 GIL），生态仍在成熟中，默认发行版仍有 GIL

## 和 asyncio / 多进程怎么选

| 场景 | 做法 |
|---|---|
| 阻塞型第三方库、改造成本高 | `threading` / `ThreadPoolExecutor` |
| 高并发网络 I/O、能用异步库 | `asyncio`（更轻） |
| CPU 密集算力 | `multiprocessing` / 进程池 |
| 已在事件循环里，偶发阻塞调用 | `asyncio.to_thread(...)` |

```python
# 在 asyncio 里临时借用线程（不必自己管 Thread）
import asyncio
import time

def blocking() -> str:
    time.sleep(1)
    return "ok"

async def main() -> None:
    print(await asyncio.to_thread(blocking))

asyncio.run(main())
```

## 常见坑

1. **忘了 `join`**  
   主线程跑完就退出，非 daemon 线程会拖住进程；daemon 则可能被直接掐掉。明确「等谁结束」。

2. **共享 list / dict 不加锁**  
   `append` 等多数操作在 CPython 上碰巧原子，但业务逻辑组合（读改写）不安全。共享可变状态用 `Lock`，或改用 `Queue`。

3. **在持锁时做慢 I/O**  
   其它线程全堵在锁上，并发名存实亡。

4. **对同一 `Thread` 调两次 `start`**  
   会抛 `RuntimeError`。要再跑就新建 `Thread`。

5. **用线程加速纯 Python CPU 循环**  
   受 GIL 限制，几乎无效；改进程池或把热点丢给原生扩展。

6. **异常在子线程里「消失」**  
   `target` 里未捕获的异常默认只打印到 stderr，主线程不知道。用 `ThreadPoolExecutor` 的 `future.result()` 会重新抛出；或自己包一层把错误放进 `Queue`。

7. **daemon 线程里做必须完成的收尾**  
   进程退出时可能来不及 `flush` / 关资源。关键工作用非 daemon + `join`，或注册 `atexit` / 显式关闭协议。

## 对比小结

| | 单线程同步 | threading | asyncio | multiprocessing |
|---|---|---|---|---|
| 切换代价 | 无 | 线程切换，偏重 | 协程切换，很轻 | 进程切换 + 序列化，更重 |
| 适合 | 逻辑简单 | 阻塞 I/O、少量并行 | 高并发 I/O | CPU 密集 |
| 共享状态 | 自然 | 需锁 / 队列 | 单线程协作，少锁 | 默认不共享，用 Queue/管道 |
| CPU 并行 | 否 | 受 GIL 限 | 否 | 是（多核） |
| 典型入口 | 直接调用 | `Thread` / 线程池 | `asyncio.run` | `Process` / 进程池 |

## 实践建议

1. **优先 `ThreadPoolExecutor`**，少手写一堆 `Thread` + 自己拼结果。
2. **线程间传数据用 `queue.Queue`**，少共享可变全局变量。
3. **必须共享时用 `with lock`**，锁粒度尽量小。
4. **先分清瓶颈**：阻塞 I/O → 线程或 asyncio；CPU → 多进程。
5. **限制并发数**（`max_workers` / `Semaphore`），避免把对端或本机打满。
6. **对外请求设超时**，线程挂死比协程挂死更难排查。
7. **能 asyncio 就别堆上千线程**；线程适合「阻塞库 + 中等并发」。
