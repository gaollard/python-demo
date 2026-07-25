# pathlib

`pathlib` 用**面向对象**的方式操作路径（Python 3.4+ 标准库）。路径是 `Path` 对象，而不是到处拼接的字符串；跨平台（POSIX / Windows）行为也更统一。日常文件路径操作优先用它，而不是 `os.path`。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| `PurePath` | 纯路径运算，不访问磁盘 | `PurePath("a") / "b.txt"` |
| `Path` | 带 I/O 的路径（`PurePath` 子类） | `Path("data") / "out.txt"` |
| `/` 运算符 | 拼接路径段（比 `os.path.join` 直观） | `Path.home() / "docs" / "a.md"` |
| 路径部件 | `name` / `stem` / `suffix` / `parent` 等 | `p.suffix == ".txt"` |
| 具体实现 | `PosixPath` / `WindowsPath` | 按当前系统自动选择 |

关系可以记成：

```
字符串 / 其它 Path
        │
        ▼
    Path(...)          ← 构造路径对象
        │
        ├─ 纯运算：/ 、.parent、.with_suffix ...（不碰磁盘）
        │
        └─ I/O：exists / read_text / mkdir / glob ...（访问文件系统）
```

## 为什么需要 pathlib

`os.path` 写法偏过程式，字符串拼接容易出错：

```python
import os

base = "/tmp/project"
path = os.path.join(base, "data", "out.txt")
name = os.path.basename(path)
stem, ext = os.path.splitext(name)
parent = os.path.dirname(path)
```

`pathlib` 把路径当成对象，读写也更直接：

```python
from pathlib import Path

path = Path("/tmp/project") / "data" / "out.txt"
print(path.name)      # out.txt
print(path.stem)      # out
print(path.suffix)    # .txt
print(path.parent)    # /tmp/project/data

path.write_text("hello", encoding="utf-8")
print(path.read_text(encoding="utf-8"))  # hello
```

## 创建路径

```python
from pathlib import Path

p1 = Path("a/b/c.txt")           # 相对路径
p2 = Path("/tmp", "a", "b.txt")  # 多段构造
p3 = Path.home()                 # 用户主目录
p4 = Path.cwd()                  # 当前工作目录
p5 = Path(__file__).resolve()    # 当前脚本的绝对路径（脚本文件里常用）

print(p1)                        # a/b/c.txt
print(p3)                        # /Users/...
```

相对 / 绝对：

```python
from pathlib import Path

rel = Path("data/out.txt")
print(rel.is_absolute())         # False
print(rel.absolute())            # 拼上 cwd，不解析符号链接
print(rel.resolve())             # 绝对路径，并解析 .. 与符号链接
```

`resolve()` 会访问文件系统；路径不存在时，较新版本默认仍可解析「逻辑」绝对路径，行为以你本机 Python 版本文档为准。需要「确定存在」时再配合 `exists()`。

## 拼接与拆解

推荐用 `/`，左右可以是 `Path` 或 `str`：

```python
from pathlib import Path

base = Path("/tmp/project")
file = base / "logs" / "app.log"
print(file)                      # /tmp/project/logs/app.log

# 等价于：
file2 = base.joinpath("logs", "app.log")
```

常用属性：

```python
from pathlib import Path

p = Path("/tmp/project/data/report.tar.gz")

print(p.name)        # report.tar.gz   最后一段
print(p.stem)        # report.tar      去掉最后一个后缀
print(p.suffix)      # .gz             最后一个后缀
print(p.suffixes)    # ['.tar', '.gz'] 全部后缀
print(p.parent)      # /tmp/project/data
print(p.parts)       # ('/', 'tmp', 'project', 'data', 'report.tar.gz')
print(p.anchor)      # /               根锚点（Windows 可能是 C:\）
```

改名不改目录：

```python
from pathlib import Path

p = Path("/tmp/a/photo.JPG")
print(p.with_name("new.png"))     # /tmp/a/new.png
print(p.with_stem("cover"))       # /tmp/a/cover.JPG   （3.9+）
print(p.with_suffix(".png"))      # /tmp/a/photo.png
```

相对路径：

```python
from pathlib import Path

full = Path("/tmp/project/src/main.py")
root = Path("/tmp/project")
print(full.relative_to(root))     # src/main.py
# full.relative_to("/other")      # ValueError：不是子路径
```

## 查询与判断

```python
from pathlib import Path

p = Path("doc.md")

print(p.exists())       # 是否存在
print(p.is_file())      # 普通文件？
print(p.is_dir())       # 目录？
print(p.is_symlink())   # 符号链接？
print(p.stat().st_size) # 字节大小（不存在会抛 FileNotFoundError）
```

匹配模式（不遍历磁盘，只看路径字符串）：

```python
from pathlib import Path

p = Path("images/cat.png")
print(p.match("*.png"))           # True
print(p.match("images/*.png"))    # True
```

## 读写文件

小文件直接读写最省事：

```python
from pathlib import Path

p = Path("notes.txt")
p.write_text("第一行\n第二行\n", encoding="utf-8")
text = p.read_text(encoding="utf-8")
print(text)

p.write_bytes(b"\x00\x01")
data = p.read_bytes()
```

大文件或需要流式处理时，用 `open()`（仍是上下文管理器）：

```python
from pathlib import Path

p = Path("big.log")
with p.open("a", encoding="utf-8") as f:
    f.write("one more line\n")
```

## 创建 / 删除 / 移动

```python
from pathlib import Path

dir_path = Path("data/raw")
dir_path.mkdir(parents=True, exist_ok=True)  # 递归创建；已存在不报错

file_path = dir_path / "sample.txt"
file_path.touch(exist_ok=True)               # 创建空文件或更新 mtime

target = dir_path / "renamed.txt"
file_path.rename(target)                     # 同盘移动/改名
# file_path.replace(target)                  # 目标存在则覆盖

target.unlink(missing_ok=True)               # 删文件；3.8+ 可忽略不存在
# dir_path.rmdir()                           # 只能删空目录
```

删非空目录用 `shutil.rmtree`：

```python
import shutil
from pathlib import Path

shutil.rmtree(Path("data"), ignore_errors=True)
```

## 遍历目录

```python
from pathlib import Path

root = Path(".")

# 只看当前层
for child in root.iterdir():
    print(child.name, "dir" if child.is_dir() else "file")

# 通配：当前层
for p in root.glob("*.py"):
    print(p)

# 递归通配
for p in root.rglob("*.md"):
    print(p)

# 组合条件
py_files = [p for p in root.rglob("*.py") if p.is_file()]
```

`glob` / `rglob` 的模式与 shell 类似：`*` 任意段内字符，`?` 单字符，`**` 在 `glob("**/*.py")` 里也可递归（等价于 `rglob("*.py")` 的常见用法）。

## 与字符串、`os.path` 互通

需要字符串 API 时转一下即可：

```python
from pathlib import Path
import os

p = Path("a/b.txt")
s = str(p)                 # 给只接受 str 的老接口
s2 = os.fspath(p)          # 更规范：走 __fspath__
print(os.path.exists(p))   # 多数 os.path 函数也能直接吃 Path
```

`open()`、`os` 许多函数、第三方库只要支持 path-like（实现 `__fspath__`），都可以直接传 `Path`。

## 常见坑

1. **用 `+` 拼路径**  
   `Path("/tmp") + "a.txt"` 会报错。拼接用 `/` 或 `joinpath`。

2. **`stem` 对多重后缀不直观**  
   `archive.tar.gz` 的 `stem` 是 `archive.tar`，`suffix` 是 `.gz`。要完整「去掉所有后缀」需自己处理 `suffixes`。

3. **`cwd` 会变**  
   `Path("rel")` 相对的是**进程当前工作目录**，不是脚本所在目录。相对脚本定位用 `Path(__file__).resolve().parent`。

4. **`exists` 有竞态**  
   `if p.exists(): p.unlink()` 仍可能在中间被删掉而抛错。更稳：直接操作并捕获 `FileNotFoundError`，或用 `unlink(missing_ok=True)`。

5. **Windows 路径分隔符**  
   代码里写 `Path("a/b/c")` 即可，`pathlib` 会按平台处理；打印时 Windows 上可能是反斜杠，属正常。

6. **`mkdir` 默认不递归**  
   缺中间目录会 `FileNotFoundError`。需要时设 `parents=True`；允许已存在则加 `exist_ok=True`。

## 对比小结

| | 字符串 + `os.path` | `pathlib.Path` |
|---|---|---|
| 拼接 | `os.path.join` | `/` 或 `joinpath` |
| 读写文件 | 自行 `open` | `read_text` / `write_text` 等 |
| 遍历 | `os.listdir` / `os.walk` | `iterdir` / `glob` / `rglob` |
| 可读性 | 函数嵌套多 | 方法链、属性清晰 |
| 跨平台 | 需注意分隔符与 API | 同一套面向对象 API |
| 适合 | 遗留代码、极简脚本 | 新代码、路径逻辑较多时 |

经验法则：新代码优先 `Path`；只和必须收 `str` 的老接口交互时再 `str(path)`。

## 实践建议

1. **新代码统一用 `pathlib`**，少在业务里散落 `os.path.join`。
2. **拼接一律 `/`**，不要手写 `/`、`\\` 字符串拼接。
3. **小文件用 `read_text` / `write_text`**，并显式传 `encoding="utf-8"`。
4. **定位资源相对脚本**：`Path(__file__).resolve().parent / "data"`，不要假设 `cwd`。
5. **创建目录写 `parents=True, exist_ok=True`**，避免环境差异导致报错。
6. **批量找文件用 `rglob`**，再按需过滤 `is_file()` / 后缀。
7. **删目录用 `shutil.rmtree`**，`Path.rmdir` 只能删空目录。
