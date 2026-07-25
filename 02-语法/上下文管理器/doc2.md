Python 上下文管理本质上是一种资源管理机制，它确保了无论代码块是正常执行完毕还是中途发生异常，资源都能被正确、自动地释放。

它通过 with 语句实现，核心目的是解决资源泄漏问题（如文件未关闭、数据库连接未释放、锁未解锁等）。

🎯 核心原理：协议方法

任何实现了以下两个特殊方法的对象，都可以作为上下文管理器：

__enter__(self): 在进入 with 代码块时自动调用。通常用于获取资源，其返回值会被赋值给 as 后面的变量。
__exit__(self, exc_type, exc_val, exc_tb): 在离开 with 代码块时自动调用（无论是否发生异常）。通常用于释放资源。
    如果代码块正常执行，三个参数均为 None。
    如果发生异常，exc_type 是异常类型，exc_val 是异常值，exc_tb 是追踪信息。
    返回值: 返回 True 表示吞掉异常（不向外抛出），返回 False 或 None 表示异常继续向外传播。

📝 基本用法

使用 with 语句（推荐）
with open('file.txt', 'r') as f:
    content = f.read()
离开 with 块时，f.close() 会自动调用，即使 read() 抛出异常

手动实现上下文管理器
class DatabaseConnection:
    def enter(self):
        self.conn = connect_to_db()
        return self.conn

    def exit(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return False  # 不吞掉异常

with DatabaseConnection() as conn:
    conn.execute("SELECT * FROM users")

🛠️ 使用 contextlib 简化

Python 标准库提供了 contextlib 模块，可以用更简洁的方式创建上下文管理器：

@contextmanager 装饰器（最常用）
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"获取资源: {name}")
    try:
        yield name  # yield 之前的代码相当于 enter
    finally:
        print(f"释放资源: {name}")  # yield 之后的代码相当于 exit

with managed_resource("database") as res:
    print(f"使用资源: {res}")

closing() 辅助函数
对于只有 close() 方法的对象，可以直接使用：
from contextlib import closing
import urllib.request

with closing(urllib.request.urlopen('https://example.com')) as page:
    html = page.read()

⚠️ 关键注意事项

异常安全: exit 中的清理代码应该放在 try/finally 中，确保即使清理过程本身出错，资源也不会泄漏。
不要吞掉异常: 除非你明确知道自己在做什么，否则 exit 应返回 False 或 None，让异常正常传播。
嵌套上下文: with 支持同时管理多个资源：
        with open('in.txt') as fin, open('out.txt', 'w') as fout:
        fout.write(fin.read())
    
Python 3.10+ 新语法: 可以使用括号跨行书写多个上下文管理器，提高可读性：
        with (
        open('in.txt') as fin,
        open('out.txt', 'w') as fout
    ):
        fout.write(fin.read())
    

💡 总结
特性   说明
核心目的   确保资源正确释放，防止泄漏

关键字   with

协议方法   enter / exit

简化方式   @contextmanager 装饰器

适用场景   文件、网络连接、数据库、锁、临时目录等

上下文管理是 Python RAII 思想的核心体现，编写 Python 代码时应优先使用 with 语句来管理任何需要手动释放的资源。

要不要我出几道练习题，帮你巩固一下上下文管理器的写法？