# venv

`venv` 是 Python 标准库自带的**虚拟环境**工具（3.3+）。它给每个项目单独准备一套「解释器 + site-packages」，让依赖互不污染：项目 A 用 `requests==2.28`，项目 B 用 `requests==2.31`，互不影响，也不去改系统 Python。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 虚拟环境（venv） | 独立的一套 Python 运行环境目录 | `.venv/`、`venv/` |
| 基础解释器 | 创建环境时复制/链接的那个 Python | `python3.12 -m venv .venv` |
| `site-packages` | 第三方包装进去的目录 | `.venv/lib/python3.x/site-packages/` |
| 激活（activate） | 改当前 shell 的 `PATH`，让 `python`/`pip` 指向该环境 | `source .venv/bin/activate` |
| 停用（deactivate） | 退出激活，恢复原来的 PATH | `deactivate` |
| 隔离 | 默认不看系统全局包（可配置） | 干净环境，可复现 |

关系可以记成：

```
系统 Python（只当「底座」）
        │
        │  python -m venv .venv
        ▼
    .venv/
      ├── bin/python          ← 本项目用的解释器
      ├── bin/pip             ← 装包装进本环境
      └── lib/.../site-packages/
                │
                ▼
        pip install requests  ← 只影响这个项目
```

激活后，shell 里的 `python` / `pip` 都会指向 `.venv` 里的那一套。

## 为什么需要 venv

没有虚拟环境时，常见问题：

1. **全局乱装**：`sudo pip install` 污染系统 Python，升级/卸载容易把别的工具弄挂。
2. **版本冲突**：两个项目要不同版本的同一包，全局只能留一套。
3. **环境不可复现**：本机能跑，别人机器缺包或版本不对。

用 venv 之后：每个项目一个目录、一份依赖；配合 `requirements.txt`（见 `01pypi`）就能在别的机器重建同样环境。

对比一下「全局装」和「进 venv」：

```bash
# 不推荐：装到系统/用户全局
pip install requests

# 推荐：先进项目环境再装
cd myproject
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install requests
```

### `source .venv/bin/activate` 的作用

`activate` 是一个 **shell 脚本**，不是 Python 程序。前面加 `source`（等价于 `. .venv/bin/activate`）是为了让脚本在**当前 shell** 里执行，而不是开子进程跑完就丢——这样才能改掉你这个终端的环境变量。

激活后主要做了这些事：

1. **把 `.venv/bin` 插到 `PATH` 最前面**  
   之后敲 `python` / `pip`，优先找到的是环境里的，而不是系统全局的。
2. **设置 `VIRTUAL_ENV`**  
   指向环境目录（如 `/path/to/myproject/.venv`），很多工具靠它判断「当前在哪个 venv」。
3. **改提示符**（可选）  
   前面加上 `(.venv)`，方便一眼看出已激活。
4. **定义 `deactivate` 函数**  
   用来恢复原来的 `PATH` 等，退出虚拟环境。

可以自己对比：

```bash
which python                    # 激活前：多半是 /usr/bin/python3 之类
source .venv/bin/activate
which python                    # 激活后：.../myproject/.venv/bin/python
echo $VIRTUAL_ENV               # .../myproject/.venv
deactivate
which python                    # 又回到系统那个
```

注意：

- **只影响当前这个终端会话**；新开终端要重新 `source`。
- 用 `bash activate`（不 `source`）几乎没用：子进程里改的 `PATH`，父 shell 看不到。
- Windows 不用 `source`，而是跑 `.venv\Scripts\activate.bat` 或 `Activate.ps1`。
- 不想激活也可以：直接 `.venv/bin/python -m pip install ...`，效果等价且更不易装错环境。

## 基本用法

### 创建

在项目根目录：

```bash
python3 -m venv .venv
```

常用约定：目录名用 `.venv`（点开头，便于 `.gitignore`，也少和包名冲突）。也有人写 `venv`，效果一样。

指定基础解释器版本（机器上有多个 Python 时）：

```bash
python3.12 -m venv .venv
# 或
/usr/local/bin/python3.11 -m venv .venv
```

创建时可选参数：

| 参数 | 作用 |
|---|---|
| `--system-site-packages` | 能看到系统全局已装的包（一般不推荐，隔离变弱） |
| `--without-pip` | 不装 pip（少用） |
| `--clear` | 若目录已存在，先清空再创建 |
| `--upgrade` | 尽量把环境里的解释器升到与创建时一致 |

### 激活与停用

macOS / Linux：

```bash
source .venv/bin/activate
# 激活后提示符前通常有 (.venv)
deactivate
```

Windows（cmd）：

```bat
.venv\Scripts\activate.bat
deactivate
```

Windows（PowerShell）：

```powershell
.venv\Scripts\Activate.ps1
deactivate
```

激活只影响**当前这个终端会话**；新开一个终端要重新 `source` / `Activate`。

### 不激活也能用（推荐习惯）

不想改 PATH 时，直接调用环境里的解释器更稳：

```bash
.venv/bin/python -m pip install requests
.venv/bin/python main.py
.venv/bin/python -c "import sys; print(sys.executable)"
```

Windows 对应：`.venv\Scripts\python.exe`。

这和「激活后再敲 `python`」等价，但更不容易装错环境。

### 装依赖

```bash
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
# 或可编辑安装本地包
python -m pip install -e .
```

习惯用 `python -m pip`，保证 pip 和当前 `python` 是同一套（见 `01pypi/question.md`）。

### 导出与重建

```bash
# 导出当前环境已装包（应用/部署常用）
python -m pip freeze > requirements.txt

# 新机器 / 新目录重建
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

库项目更常把依赖写在 `pyproject.toml`，再用 `pip install -e ".[dev]"`，不一定只靠 `freeze`。

### 删除

虚拟环境就是一个普通目录，删掉即可：

```bash
deactivate          # 若已激活，先退出
rm -rf .venv        # Windows: rmdir /s /q .venv
```

需要时再重新 `python -m venv .venv` + 装依赖。**不要把 `.venv` 提交进 Git**，体积大且和本机路径绑定；提交 `requirements.txt` / `pyproject.toml` 即可。

`.gitignore` 示例：

```gitignore
.venv/
venv/
```

## 目录里有什么

以 Unix 为例（简化）：

```
.venv/
├── bin/
│   ├── python          → 指向基础解释器（或拷贝）
│   ├── python3
│   ├── pip / pip3
│   ├── activate        ← shell 激活脚本
│   └── ...
├── lib/
│   └── python3.x/
│       └── site-packages/   ← pip 装的包装这里
├── include/            ← 编译扩展时可能用到
└── pyvenv.cfg          ← 记录 home（基础 Python 路径）等元信息
```

`pyvenv.cfg` 里的 `home` 指向创建时的基础 Python。换机器或删了那个 Python 后，旧 `.venv` 可能失效，应重建环境。

## 和 IDE / 工具的配合

- **VS Code / Cursor**：选解释器为 `.venv/bin/python`，终端与运行都会用这套。
- **PyCharm**：Project Interpreter 指向 `.venv`。
- **Makefile / CI**：脚本里写死 `.venv/bin/python -m pytest`，不依赖「是否已 activate」。

CI 典型片段：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
```

## 和其他方案对比

| | `venv`（标准库） | `virtualenv` | `conda` | Poetry / PDM / uv |
|---|---|---|---|---|
| 来源 | 官方自带 | 第三方，功能更多 | Anaconda 生态 | 现代项目管理工具 |
| 装包 | 仍用 pip | 仍用 pip | `conda install` / 也可 pip | 自带依赖解析与锁文件 |
| 适合 | 大多数应用/脚本 | 老环境、额外选项 | 数据科学、非 Python 依赖 | 要锁文件、发布工作流时 |
| 学习成本 | 最低 | 低 | 中 | 中 |

日常学习与多数业务项目：**先会 `python -m venv` + `pip` 就够**。需要更快解析、锁文件时再上 uv / Poetry 等；它们底层往往仍会创建类似 venv 的环境目录。

## 常见坑

1. **装包时装到全局了**  
   没激活，或 `pip` 指向别的解释器。自检：

   ```bash
   which python
   which pip
   python -c "import sys; print(sys.executable)"
   python -m pip --version
   ```

2. **激活了 A 项目的环境，却在 B 目录里装包**  
   包装进了当前激活的环境，不一定是「当前目录」的环境。以 `sys.executable` 为准，或始终用 `.venv/bin/python -m pip`。

3. **把 `.venv` 提交进 Git**  
   又大又难跨机器用。只提交依赖声明，让别人自己创建环境。

4. **换了系统 Python 版本，旧 venv 半残**  
   删掉 `.venv` 用新版本重建，再 `pip install -r`。

5. **`--system-site-packages` 导致「本机有、别人没有」**  
   默认可复现性更好；除非明确要共用系统包，否则别开。

6. **Windows 执行策略拦 `Activate.ps1`**  
   可用 cmd 的 `activate.bat`，或调整 PowerShell 执行策略；也可用 `.venv\Scripts\python.exe` 直接跑，不依赖激活。

7. **在 venv 里又 `pip install` 出一个同名工具，和系统命令混淆**  
   激活后优先用环境内的可执行文件；不确定就写全路径。

## 最小工作流（记这个就行）

```bash
cd myproject
python3 -m venv .venv
source .venv/bin/activate              # 或直接用 .venv/bin/python
python -m pip install -U pip
python -m pip install -r requirements.txt
python main.py
deactivate
```

## 实践建议

1. **一个项目一个 `.venv`**，目录放在项目根，并加入 `.gitignore`。
2. **优先 `python -m venv` + `python -m pip`**，少直接敲裸的 `pip`。
3. **脚本/CI 写 `.venv/bin/python ...`**，不依赖人工是否 activate。
4. **依赖进文件**：应用用 `requirements.txt`（或锁文件）；库用 `pyproject.toml`。
5. **环境坏了就删了重建**，比在半残目录里修更省时间。
6. **和 PyPI/pip 一节连起来看**：venv 管「装到哪」，pip 管「装什么」（见 `01pypi/doc.md`）。
