# multiprocessing

`multiprocessing` 是 Python 标准库的**多进程**模块。每个子进程有独立的解释器与内存空间，**不受 GIL 限制**，适合把 **CPU 密集**计算真正跑到多核上。代价是进程更重，进程间不能像线程那样直接共享普通变量。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 进程（Process） | 独立的 OS 进程，各自有内存 | `multiprocessing.Process(target=f)` |
| 主进程 | 启动程序时的那个进程 | `multiprocessing.current_process()` |
| `start` / `join` | 启动子进程；等待结束 | `p.start(); p.join()` |
| 进程池 | 复用一组 worker，提交任务 | `ProcessPoolExecutor` / `Pool` |
| 队列 / 管道 | 进程间传数据（要可 pickle） | `Queue` / `Pipe` |
| 共享内存 | 刻意共享少量状态 | `Value` / `Array` / `SharedMemory` |
| 启动方式 | 怎么创建子进程 | `fork` / `spawn` / `forkserver` |

关系可以记成：

```
主进程
  │
  ├─ Process(target=...).start()  →  另起一个解释器跑函数
  ├─ join()                       →  等它结束
  └─ Queue / Pipe / Manager       →  传数据（默认不共享内存）
```

## 为什么需要 multiprocessing

多线程受 GIL 限制，纯 Python 的 CPU 循环很难加速（见 `threading/doc.md`）。多进程每个进程一份 GIL，可以真正并行：

```python
import time

def cpu_job(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total

def main():
    t0 = time.perf_counter()
    a = cpu_job(10_000_000)
    b = cpu_job(10_000_000)
    print(a, b, time.perf_counter() - t0)  # 串行，约 2 倍单次耗时

main()
```

改用进程池，多核能同时算：

```python
import time
from concurrent.futures import ProcessPoolExecutor

def cpu_job(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total

def main():
    t0 = time.perf_counter()
    with ProcessPoolExecutor(max_workers=2) as pool:
        a, b = pool.map(cpu_job, [10_000_000, 10_000_000])
    print(a, b, time.perf_counter() - t0)  # 接近单次耗时（机器有多核时）

if __name__ == "__main__":
    main()
```

要点：`multiprocessing` 适合 **CPU 密集**；大量阻塞 I/O 更优先 `threading` / `asyncio`。

## 基本用法

### 创建与启动

```python
import multiprocessing as mp
import time

def worker(n: int) -> None:
    print(f"start {n} pid={mp.current_process().pid}")
    time.sleep(0.5)
    print(f"end {n}")

def main():
    p = mp.Process(target=worker, args=(1,), name="worker-1")
    p.start()                  # 真正拉起子进程
    p.join()                   # 等它结束
    print("exitcode", p.exitcode)

if __name__ == "__main__":     # Windows / macOS spawn 下几乎必须
    main()
```

用类继承也可以（少见）：

```python
import multiprocessing as mp

class Worker(mp.Process):
    def __init__(self, n: int):
        super().__init__()
        self.n = n

    def run(self) -> None:     # start() 会调用 run()
        print("work", self.n)

def main():
    Worker(1).start()

if __name__ == "__main__":
    main()
```

日常更推荐 `target=` 函数，或直接上进程池。

### `if __name__ == "__main__"` 为什么重要

在 `spawn`（Windows 默认；macOS 3.8+ 默认）下，子进程会**重新 import** 主模块。若创建进程的代码写在模块顶层，会无限递归再 spawn。

规则：所有 `Process` / `Pool` / `ProcessPoolExecutor` 的启动入口，都放进 `if __name__ == "__main__":`（或由该守卫调用的函数里）。

### 传参与取结果

`Process` 本身**不返回** `target` 的返回值。常见做法：

1. 用 `multiprocessing.Queue`  
2. 用 `Manager` 里的容器  
3. 用 `concurrent.futures.ProcessPoolExecutor`（最省事）

```python
from concurrent.futures import ProcessPoolExecutor, as_completed

def job(n: int) -> int:
    return n * n

def main():
    with ProcessPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(job, i) for i in range(5)]
        for f in as_completed(futures):
            print(f.result())  # 完成顺序不定

if __name__ == "__main__":
    main()
```

`map` 写法（按入参顺序拿结果）：

```python
from concurrent.futures import ProcessPoolExecutor

def job(n: int) -> int:
    return n * n

def main():
    with ProcessPoolExecutor(max_workers=4) as pool:
        print(list(pool.map(job, range(5))))  # [0, 1, 4, 9, 16]

if __name__ == "__main__":
    main()
```

### 守护进程（daemon）

```python
import multiprocessing as mp
import time

def background() -> None:
    while True:
        print("tick")
        time.sleep(1)

def main():
    p = mp.Process(target=background, daemon=True)
    p.start()
    time.sleep(2.5)
    # 主进程结束 → daemon 子进程会被终止

if __name__ == "__main__":
    main()
```

规则与线程类似：需要可靠收尾时，**不要**只靠 daemon；用 `join`、显式发结束信号，并在 `try/finally` 里清理。

注意：daemon 进程**不能再创建子进程**。

## 进程间通信

进程默认**不共享**普通 Python 对象。传数据必须可被 **pickle**（或走共享内存）。

### `Queue`：进程间传数据（优先推荐）

```python
import multiprocessing as mp

def producer(q: mp.Queue) -> None:
    for i in range(3):
        q.put(f"item-{i}")
    q.put(None)                # 结束哨兵

def consumer(q: mp.Queue) -> None:
    while True:
        item = q.get()
        if item is None:
            break
        print("consume", item)

def main():
    q: mp.Queue = mp.Queue()
    p1 = mp.Process(target=producer, args=(q,))
    p2 = mp.Process(target=consumer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == "__main__":
    main()
```

注意：这里用的是 `multiprocessing.Queue`，不是 `queue.Queue`（后者只适合线程）。

### `Pipe`：双向管道

```python
import multiprocessing as mp

def worker(conn: mp.connection.Connection) -> None:
    msg = conn.recv()
    conn.send(msg.upper())
    conn.close()

def main():
    parent, child = mp.Pipe()
    p = mp.Process(target=worker, args=(child,))
    p.start()
    parent.send("hello")
    print(parent.recv())       # HELLO
    p.join()

if __name__ == "__main__":
    main()
```

两端各拿一个 connection；两端同时读写同一端要小心死锁。多生产者/多消费者一般更适合 `Queue`。

### `Manager`：代理对象（方便但慢）

```python
import multiprocessing as mp

def bump(d: dict, key: str) -> None:
    d[key] = d.get(key, 0) + 1

def main():
    with mp.Manager() as manager:
        d = manager.dict()
        procs = [mp.Process(target=bump, args=(d, "n")) for _ in range(4)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        print(dict(d))         # 可能小于 4：dict 代理的「读改写」仍要自己同步

if __name__ == "__main__":
    main()
```

`Manager` 通过服务进程 + 代理实现共享 list/dict 等，**方便但不适合高频热路径**。高频共享整数/数组优先 `Value` / `Array` / `SharedMemory`。

### `Value` / `Array`：共享内存标量与数组

```python
import multiprocessing as mp

def bump(counter: mp.Value, lock: mp.Lock) -> None:
    for _ in range(100_000):
        with lock:
            counter.value += 1

def main():
    counter = mp.Value("i", 0)  # i = signed int
    lock = mp.Lock()
    procs = [mp.Process(target=bump, args=(counter, lock)) for _ in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(counter.value)       # 400000

if __name__ == "__main__":
    main()
```

## 同步原语

多进程也有 `Lock`、`Event`、`Condition`、`Semaphore`，API 与 `threading` 类似，但作用于**进程间**：

```python
import multiprocessing as mp
import time

sem = mp.Semaphore(2)

def access(n: int) -> None:
    with sem:
        print("in", n)
        time.sleep(0.5)
        print("out", n)

def main():
    procs = [mp.Process(target=access, args=(i,)) for i in range(5)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()

if __name__ == "__main__":
    main()
```

原则：能靠「任务进、结果出」的 `Queue` / 进程池解决，就少共享可变状态。

## 启动方式（start method）

| 方式 | 含义 | 常见平台 |
|---|---|---|
| `spawn` | 新解释器，重新 import | Windows 默认；macOS 3.8+ 默认 |
| `fork` | 拷贝父进程内存（写时复制） | 传统 Linux 默认 |
| `forkserver` | 先起一个 server，再 fork 出 worker | 可选，兼顾安全与速度 |

```python
import multiprocessing as mp

def main():
    print(mp.get_start_method())
    # mp.set_start_method("spawn")  # 整个程序只能设一次

if __name__ == "__main__":
    main()
```

注意：

- `fork` 后，父进程里已有的锁/线程状态可能不安全；有多线程时再 `fork` 尤其危险。
- 跨平台代码优先按 `spawn` 心态写：目标函数要可 pickle，入口用 `__main__` 守卫。
- 传给子进程的函数、参数必须能被 pickle（局部函数、lambda、未绑定好的闭包常会挂）。

## 和 threading / asyncio 怎么选

| 场景 | 做法 |
|---|---|
| CPU 密集算力（纯 Python 循环、重计算） | `multiprocessing` / `ProcessPoolExecutor` |
| 阻塞型 I/O、改造成本高 | `threading` / `ThreadPoolExecutor` |
| 高并发网络 I/O、能用异步库 | `asyncio` |
| 已在事件循环里，偶发 CPU 重活 | `asyncio` + `ProcessPoolExecutor`（`loop.run_in_executor`） |

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def cpu_job(n: int) -> int:
    return sum(i * i for i in range(n))

async def main() -> None:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_job, 1_000_000)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## 常见坑

1. **忘了 `if __name__ == "__main__"`**  
   `spawn` 下会递归创建进程，或直接报 RuntimeError。

2. **目标函数 / 参数不可 pickle**  
   嵌套函数、lambda、某些闭包、带锁的对象，常导致启动失败。把 worker 写成模块级函数。

3. **把 `queue.Queue` 当进程队列用**  
   线程队列不能跨进程。进程间用 `multiprocessing.Queue` 或 `Manager().Queue()`。

4. **大数据反复 pickle**  
   每个任务参数/返回值都要序列化。任务太碎、数据太大时，开销可能吃掉并行收益。考虑分块、共享内存、或减少往返。

5. **进程数不是越多越好**  
   CPU 密集一般先试 `os.cpu_count()` 左右；过多会上下文切换和内存爆炸。

6. **子进程里的异常**  
   手写 `Process` 时，异常默认打到子进程 stderr，主进程不一定知道。用 `ProcessPoolExecutor` 的 `future.result()` 会重新抛出。

7. **在 Jupyter / 交互环境乱开进程**  
   `__main__` 与 pickle 行为更绕，教学演示优先用脚本文件跑。

8. **`terminate()` / `kill()` 硬杀**  
   可能留下未刷盘文件、未释放的共享资源。优先发「结束」消息让 worker 自己退出，再 `join`。

## 对比小结

| | 单进程同步 | threading | asyncio | multiprocessing |
|---|---|---|---|---|
| 切换代价 | 无 | 线程切换，偏重 | 协程切换，很轻 | 进程切换 + 序列化，更重 |
| 适合 | 逻辑简单 | 阻塞 I/O | 高并发 I/O | CPU 密集 |
| 共享状态 | 自然 | 需锁 / 队列 | 单线程协作，少锁 | 默认不共享，用 Queue/管道 |
| CPU 并行 | 否 | 受 GIL 限 | 否 | 是（多核） |
| 典型入口 | 直接调用 | `Thread` / 线程池 | `asyncio.run` | `Process` / 进程池 |

## 实践建议

1. **优先 `ProcessPoolExecutor`**，少手写一堆 `Process` + 自己拼结果。
2. **进程间传数据用 `Queue`**，少上 `Manager` 字典做热路径。
3. **入口永远用 `__main__` 守卫**；worker 写成模块级可 pickle 函数。
4. **先分清瓶颈**：CPU → 多进程；阻塞 I/O → 线程；高并发 I/O → asyncio。
5. **控制进程数与任务粒度**：太碎则 pickle 吃掉收益；太大则负载不均。
6. **测一下再信**：用 `time.perf_counter()` 对比串行 vs 进程池，确认真有加速。
7. **能向量化 / 丢给 numpy、C 扩展时**，有时单进程更快，不必强上多进程。
