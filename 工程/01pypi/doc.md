# PyPI

PyPI（**Python Package Index**，https://pypi.org）是 Python 的**公共包仓库**。你平时写的 `pip install requests`，默认就是从这里下载安装包。自己写的库也可以打包上传，让别人（或别的机器）一行命令装上。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 包名（project name） | PyPI 上的项目名，全局唯一 | `requests`、`numpy` |
| 发行版（distribution） | 一次可安装的构建产物 | `.whl` / `.tar.gz` |
| wheel | 预构建二进制包，安装快 | `foo-1.0.0-py3-none-any.whl` |
| sdist | 源码包，安装时可能要现场构建 | `foo-1.0.0.tar.gz` |
| 索引（index） | 包列表与下载地址的源 | PyPI / TestPyPI / 私有源 |
| `pip` | 客户端：搜、装、卸、列出版本 | `pip install foo` |
| 版本号 | 通常用 PEP 440 | `1.2.3`、`1.2.3a1`、`1.2.3.post1` |

关系可以记成：

```
源码项目（pyproject.toml + 代码）
        │
        ▼
    python -m build          ← 打出 sdist / wheel
        │
        ▼
    twine upload             ← 上传到 PyPI / TestPyPI
        │
        ▼
    pip install 包名         ← 别人从索引下载安装
```

## 为什么需要 PyPI

没有公共索引时，依赖只能靠拷贝源码、`git clone`、或自己搭服务器。PyPI 把「发现 → 下载 → 安装 → 版本约束」标准化了：

```bash
# 装指定版本
pip install "requests>=2.28,<3"

# 装开发版 / 本地可编辑
pip install -e .

# 从私有源装（公司内网常见）
pip install foo --index-url https://pypi.example.com/simple/
```

要点：**写库给别人用、或给自己多台机器复用**，就走上 PyPI（或兼容的私有索引）；只在本机脚本跑，用 venv + `requirements.txt` 往往就够（见 `工程/02venv`）。

## 日常使用：找包与安装

### 搜索与查看

```bash
# 网页：https://pypi.org ，搜包名即可
pip index versions requests          # 看有哪些版本（pip 新版本）
pip show requests                    # 已安装包的元信息
pip list                             # 当前环境已装列表
```

### 安装与卸载

```bash
python -m pip install requests
python -m pip install "numpy==1.26.4"
python -m pip uninstall requests
```

习惯写成 `python -m pip ...`，避免装到「另一个 Python」里（系统自带的 `pip` 和当前解释器可能不是一套）。

### 依赖文件

小项目常用 `requirements.txt`：

```text
requests>=2.28
httpx==0.27.0
```

```bash
pip install -r requirements.txt
```

库项目更常见把依赖写在 `pyproject.toml` 的 `[project]` 里（见下文），再用 `pip install .` / `pip install -e .`。

### 国内镜像（可选）

公网慢时可用镜像，例如：

```bash
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
```

长期可写到 `~/.pip/pip.conf`（或项目级配置），但**上传到官方 PyPI 仍走 pypi.org**，镜像只加速下载。

## 自己发一个包（现代写法）

下面用 **setuptools + pyproject.toml** 走一遍最小流程。包名假设叫 `demo-hello`，导入名 `demo_hello`。

### 1. 目录结构

```
demo-hello/
├── pyproject.toml
├── README.md
├── src/
│   └── demo_hello/
│       ├── __init__.py
│       └── greet.py
└── tests/
    └── test_greet.py
```

`src/` 布局的好处：强制你用「安装后再测」，避免误 import 到仓库里的裸源码。

`src/demo_hello/greet.py`：

```python
def hello(name: str = "world") -> str:
    return f"hello, {name}"
```

`src/demo_hello/__init__.py`：

```python
from .greet import hello

__all__ = ["hello"]
__version__ = "0.1.0"
```

### 2. `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "demo-hello"
version = "0.1.0"
description = "A tiny demo package"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [{ name = "You", email = "you@example.com" }]
dependencies = [
  # "requests>=2.28",
]

[project.optional-dependencies]
dev = ["pytest>=8"]

[project.urls]
Homepage = "https://github.com/you/demo-hello"

[tool.setuptools.packages.find]
where = ["src"]
```

说明：

- `name`：PyPI 上的**项目名**（可有连字符）
- 导入时用的是包目录名 `demo_hello`（下划线），两者可以不同，但别起冲突名
- `requires-python`：声明兼容的 Python 版本，pip 会据此过滤

### 3. 本地可编辑安装

```bash
cd demo-hello
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install -e ".[dev]"  # 改代码立刻生效，适合开发
pytest
```

验证：

```python
from demo_hello import hello
print(hello("pypi"))  # hello, pypi
```

### 4. 构建

```bash
python -m pip install build
python -m build
```

会在 `dist/` 生成类似：

```
demo_hello-0.1.0.tar.gz
demo_hello-0.1.0-py3-none-any.whl
```

先在干净 venv 里试装：

```bash
python -m pip install dist/demo_hello-0.1.0-py3-none-any.whl
```

### 5. 上传：先 TestPyPI，再正式 PyPI

1. 注册账号：https://pypi.org 与 https://test.pypi.org（**两套账号，不共用**）
2. 建议创建 **API token**，不要用账号密码长期上传
3. 配置 `~/.pypirc`（可选）：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...你的正式 token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...你的测试 token
```

上传：

```bash
python -m pip install twine
python -m twine upload --repository testpypi dist/*
# 确认无误后再：
python -m twine upload dist/*
```

从 TestPyPI 试装：

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ demo-hello
```

`--extra-index-url` 用来拉依赖（TestPyPI 上可能没有你依赖的第三方包）。

### 6. 发新版本

改 `pyproject.toml` 里的 `version`（或改用动态版本工具），重新 `build`，再 `twine upload`。

**同一版本号只能上传一次**；传错了通常只能 yank（标记「不推荐」）或升版本号重发，不能直接覆盖。

## 包名、版本与依赖约束

### 版本号（PEP 440 常用形态）

| 写法 | 含义 |
|---|---|
| `1.2.3` | 正式版 |
| `1.2.3a1` / `b1` / `rc1` | 预发布 |
| `1.2.3.post1` | 修订发行（不改代码逻辑时少用） |
| `1.2.3.dev1` | 开发中 |

依赖里常用：

```text
package>=1.2,<2          # 兼容 1.x
package~=1.2.3           # 约等于：>=1.2.3, ==1.2.*
package==1.2.3           # 钉死（应用/复现环境更常见）
```

库尽量写宽松下限 + 主版本上限；应用/部署环境更常钉死或锁文件（`pip freeze` / uv / poetry lock）。

### 项目名已被占用？

上 PyPI 前先搜：https://pypi.org/project/你的名字/  
名字冲突就换名；导入名（`import xxx`）也尽量别和标准库、热门第三方撞车。

## 常见坑

1. **`pip` 装到了别的解释器**  
   用 `python -m pip`，并用 `which python` / `python -c "import sys; print(sys.executable)"` 确认环境。

2. **全局乱装，污染系统 Python**  
   项目一律进 venv（见 `工程/02venv`），再 `pip install`。

3. **只传了源码目录，没声明包数据**  
   非 `.py` 资源（模板、json）要在构建配置里声明，否则 wheel 里没有这些文件。

4. **在仓库根目录直接 `import`，一打包就挂**  
   用 `src/` 布局 + `pip install -e .`，测试装进去的包，而不是偶然 import 到本地文件夹。

5. **版本号重复上传**  
   改代码必须 bump version。传错可用 yank，但已下载的缓存仍可能存在。

6. **把密钥写进仓库**  
   `~/.pypirc`、token、密码不要提交 Git。用环境变量或本地配置。

7. **第一次就上传正式 PyPI**  
   先 TestPyPI 走通「构建 → 上传 → 干净环境安装」。

8. **包名与导入名混淆**  
   `pip install demo-hello`，代码里是 `import demo_hello`。文档里写清楚。

9. **依赖漏写**  
   你本机碰巧装着，别人干净环境一装就 `ModuleNotFoundError`。构建前在新 venv 验证。

## 对比小结

| | 只本地用 | 发到 PyPI | 私有索引 |
|---|---|---|---|
| 目标 | 本机脚本 / 小项目 | 公开复用 | 公司内部分发 |
| 依赖声明 | `requirements.txt` | `pyproject.toml` | 同左，源不同 |
| 安装方式 | `pip install -r` / `-e .` | `pip install 包名` | `pip install` + `--index-url` |
| 上传工具 | 不需要 | `build` + `twine` | 视平台而定 |

## 实践建议

1. **新库一律 `pyproject.toml`**，别再新建遗留的纯 `setup.py` 项目（需要时再补兼容）。
2. **开发用 `pip install -e .`**，发布前 `python -m build` + 干净 venv 试装。
3. **先 TestPyPI，再正式 PyPI**；用 API token，不要把密码写进脚本。
4. **版本只增不改**：一次上传绑定一个版本号。
5. **文档写清**：安装名、`import` 名、`requires-python`、最小示例。
6. **应用锁依赖、库放宽依赖**：避免把传递依赖钉死到让下游无法安装。
7. **和 venv 一起用**：每个项目独立环境，再谈装包与发包（下一节 `02venv`）。
