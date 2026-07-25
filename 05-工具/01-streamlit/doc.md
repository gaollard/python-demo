https://docs.streamlit.io

# Streamlit

Streamlit 是用 **纯 Python** 快速搭数据应用 / 内部工具的库。写脚本式代码（从上到下执行），不用写 HTML / JS / 前端路由，浏览器里就能交互：改滑块、点按钮，脚本会**整页重跑**，界面跟着更新。

适合：数据分析看板、模型 Demo、内部运维小工具、快速原型。不适合：复杂多角色权限系统、强定制 UI 的生产级前端。

## 核心概念

| 概念 | 含义 | 典型例子 |
|---|---|---|
| 脚本即应用 | `.py` 从上到下执行一次 = 渲染一帧 UI | `streamlit run app.py` |
| 重跑（rerun） | 用户点控件后，整个脚本再跑一遍 | 改 `st.slider` → 全脚本重执行 |
| Widget | 输入控件，返回当前值 | `st.button` / `st.selectbox` / `st.text_input` |
| `st.session_state` | 跨次重跑仍保留的状态字典 | 计数器、登录标记、表单草稿 |
| 缓存 | 避免重跑时重复算贵操作 | `@st.cache_data` / `@st.cache_resource` |
| 布局容器 | 控制元素放哪 | `st.columns` / `st.sidebar` / `st.tabs` |

关系可以记成：

```
浏览器操作（改控件 / 点按钮）
        │
        ▼
  Streamlit 服务端触发 rerun
        │
        ▼
  从上到下重新执行 app.py
        │
        ├─ 读 widget 当前值
        ├─ 读 / 写 st.session_state（跨次保留）
        ├─ 命中缓存则跳过贵计算
        └─ 重新画出整页 UI
```

关键心智模型：**不是**「事件回调改局部 DOM」，而是「交互 → 整脚本再跑一遍 → 新 UI」。

## 为什么需要 Streamlit

传统做法：Flask/Django 写后端 + 再写前端，或 Jupyter 只能笔记本交互，分享成本高。

Streamlit 把「Python 算出结果」和「给别人点一点用」之间的距离压到最短：

1. **零前端**：只写 Python，自动出 Web UI。
2. **数据友好**：原生吃 DataFrame、图表（Plotly / Altair / Matplotlib）。
3. **迭代快**：改代码保存，浏览器热更新。
4. **状态可控**：用 `session_state` + 缓存处理「整页重跑」带来的问题。

对比一下「纯脚本打印」和「Streamlit」：

```python
# 终端脚本：只能改参数再跑
x = 10
print(x * 2)
```

```python
# Streamlit：浏览器里拖滑块，立刻看到结果
import streamlit as st

x = st.slider("x", 0, 100, 10)
st.write("结果：", x * 2)
```

## 安装与启动

```bash
python -m pip install streamlit
streamlit hello                    # 官方示例，确认安装成功
streamlit run app.py               # 跑你的应用
```

常用选项：

```bash
streamlit run app.py --server.port 8501
streamlit run app.py --server.headless true   # 服务器上不自动开浏览器
```

默认地址：`http://localhost:8501`。

## 最小应用

```python
# app.py
import streamlit as st

st.title("Hello Streamlit")
name = st.text_input("名字", value="world")
st.write(f"Hello, {name}!")
```

```bash
streamlit run app.py
```

## 常用展示

```python
import streamlit as st
import pandas as pd

st.title("标题")
st.header("一级小节")
st.subheader("二级小节")
st.markdown("支持 **Markdown** 和 $E=mc^2$")
st.code("print('hi')", language="python")
st.json({"ok": True, "n": 1})

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
st.dataframe(df)          # 可交互表格
st.table(df)              # 静态表
st.metric("销量", 1200, delta="+12%")
st.line_chart(df)         # 快速图表（基于 Altair）
```

## 常用输入控件

```python
import streamlit as st

st.button("点我")                          # 返回 True / False（当次重跑）
st.checkbox("同意协议")
st.radio("颜色", ["红", "绿", "蓝"])
st.selectbox("城市", ["北京", "上海", "深圳"])
st.multiselect("标签", ["A", "B", "C"])
st.slider("分数", 0, 100, 60)
st.number_input("数量", min_value=0, value=1)
st.text_input("用户名")
st.text_area("备注")
st.date_input("日期")
st.file_uploader("上传 CSV", type=["csv"])
```

要点：

- 控件的**返回值**就是当前 UI 上的值；不要想成「注册回调」。
- `st.button` 只在**被点击的那一次 rerun** 里为 `True`，下一轮又变回 `False`。要记「点过」必须写进 `session_state`。

## 布局

```python
import streamlit as st

# 侧边栏
city = st.sidebar.selectbox("城市", ["北京", "上海"])

# 分栏
left, right = st.columns(2)
left.write("左")
right.write("右")

# 标签页
tab1, tab2 = st.tabs(["概览", "明细"])
with tab1:
    st.write("概览内容")
with tab2:
    st.write("明细内容")

# 折叠
with st.expander("高级选项"):
    st.write("默认收起")
```

页面配置（建议放在脚本最上面，且只调一次）：

```python
import streamlit as st

st.set_page_config(
    page_title="我的看板",
    page_icon="📊",
    layout="wide",          # 或 "centered"
    initial_sidebar_state="expanded",
)
```

## session_state：跨次重跑的状态

整页重跑会把普通局部变量清掉。需要「记住」的东西放进 `st.session_state`：

```python
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

col1, col2 = st.columns(2)
if col1.button("+1"):
    st.session_state.count += 1
if col2.button("清零"):
    st.session_state.count = 0

st.write("当前计数：", st.session_state.count)
```

也可以给控件绑 key，值会自动进 `session_state`：

```python
import streamlit as st

st.text_input("名字", key="name")
st.write("你输入了：", st.session_state.get("name", ""))
```

常见模式：用按钮改状态后立刻 `st.rerun()`，强制再跑一帧（多数情况改 `session_state` 后 Streamlit 会自动 rerun，显式调用用于特殊流程）。

## 缓存：别在每次 rerun 里重算

每次交互都重跑脚本，所以加载大文件、调远程 API、训模型必须缓存。

### `@st.cache_data` —— 缓存「数据」

适合：可序列化的返回值（DataFrame、dict、list…）。参数变了才重算。

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

df = load_csv("data.csv")
st.dataframe(df)
```

### `@st.cache_resource` —— 缓存「资源 / 连接」

适合：数据库连接、ML 模型、全局单例（不应每个用户复制一份大数据时也常用）。

```python
import streamlit as st

@st.cache_resource
def get_model():
    # 假设计算很重
    return {"weights": [0.1, 0.2, 0.3]}

model = get_model()
st.write(model)
```

怎么选：

| 装饰器 | 缓存什么 | 典型场景 |
|---|---|---|
| `cache_data` | 函数返回值的拷贝 | 读文件、查询结果、预处理 |
| `cache_resource` | 同一对象引用 | DB engine、Torch 模型、客户端 |

清缓存：侧边栏菜单「Clear cache」，或代码里 `load_csv.clear()`。

## 表单：一次提交多个输入

没有 form 时，每个控件一改就触发 rerun。表单把多个输入攒到一起，点提交才重跑：

```python
import streamlit as st

with st.form("login"):
    user = st.text_input("用户名")
    pwd = st.text_input("密码", type="password")
    ok = st.form_submit_button("登录")

if ok:
    if user == "admin" and pwd == "secret":
        st.success("登录成功")
    else:
        st.error("账号或密码错误")
```

## 文件上传与下载

```python
import streamlit as st
import pandas as pd

file = st.file_uploader("上传 CSV", type=["csv"])
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df)
    st.download_button(
        "下载结果",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="out.csv",
        mime="text/csv",
    )
```

## 简单图表示例

```python
import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"],
)
st.line_chart(chart_data)
st.bar_chart(chart_data)
st.area_chart(chart_data)

# 需要更强定制时用 plotly / altair，再 st.plotly_chart / st.altair_chart
```

## 多页面应用

目录约定：

```
myapp/
  Home.py                 # 入口：streamlit run Home.py
  pages/
    1_概览.py
    2_明细.py
```

`pages/` 下的每个 `.py` 自动出现在侧边栏。页面之间靠 `st.session_state` 共享状态（同一浏览器会话）。

也可以在单文件里用 `st.navigation` / `st.Page`（较新 API）组织多页，按你安装的 Streamlit 版本文档选用即可。

## 和「普通 Web 框架」差在哪

| | Streamlit | Flask / FastAPI + 前端 |
|---|---|---|
| 写法 | 脚本自上而下 | 路由 + 模板 / SPA |
| 交互模型 | 整页 rerun | 请求 / 响应或前端状态 |
| 适合 | 数据工具、Demo、内部看板 | 复杂业务、对外产品 |
| 前端自由度 | 低（组件库约束） | 高 |
| 上手成本 | 极低 | 高 |

经验法则：先问「是不是主要给自己或同事看数据 / 调参？」——是，优先 Streamlit；要做成正式产品站，再上完整 Web 栈。

## 常见坑

1. **按钮只亮一瞬间**  
   `st.button` 为 `True` 只持续当次 rerun。要累积效果，写入 `session_state`。

2. **每次交互都重新读库 / 读大文件**  
   用 `@st.cache_data` / `@st.cache_resource`，否则又慢又容易打爆后端。

3. **在循环里狂建同名 widget**  
   同一 rerun 里 widget 的 `key` 必须唯一，否则报错。

4. **把密钥写进代码并部署**  
   用 `st.secrets`（`.streamlit/secrets.toml`）或环境变量，不要提交到 git。

5. **以为变量赋值能「记住」**  
   普通 Python 变量每次 rerun 都会重新初始化；跨交互状态只用 `session_state`。

6. **`st.set_page_config` 不在最前**  
   必须在其它 `st.*` 之前调用，且每个脚本一次。

## 最小可运行看板骨架

```python
# app.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="销售看板", layout="wide")
st.title("销售看板")

@st.cache_data
def load_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    return pd.DataFrame(
        {
            "day": pd.date_range("2024-01-01", periods=30, freq="D"),
            "sales": rng.integers(80, 200, size=30),
            "city": rng.choice(["北京", "上海", "深圳"], size=30),
        }
    )

df = load_data()

city = st.sidebar.multiselect(
    "城市",
    options=sorted(df["city"].unique()),
    default=sorted(df["city"].unique()),
)
view = df[df["city"].isin(city)] if city else df.iloc[0:0]

c1, c2, c3 = st.columns(3)
c1.metric("总销量", int(view["sales"].sum()) if len(view) else 0)
c2.metric("日均", round(view["sales"].mean(), 1) if len(view) else 0)
c3.metric("记录数", len(view))

st.line_chart(view.set_index("day")["sales"])
st.dataframe(view, use_container_width=True)
```

```bash
streamlit run app.py
```

## 延伸阅读

- 官方文档：https://docs.streamlit.io/
- API 速查：https://docs.streamlit.io/develop/api-reference
- 部署：Streamlit Community Cloud / Docker 自建均可；核心仍是 `streamlit run`
