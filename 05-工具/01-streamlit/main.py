"""本地 Ollama 聊天 Demo（Streamlit）。

说明：
- 通过 Ollama 的 OpenAI 兼容接口调用本地模型
- Streamlit 每次交互都会整页重跑脚本，对话历史靠 session_state 保留
"""

import streamlit as st
from openai import OpenAI

# Ollama OpenAI 兼容 API 地址（默认端口 11434）
OLLAMA_BASE_URL = "http://localhost:11434/v1"
# Ollama 不可用时的兜底模型列表
DEFAULT_MODELS = ["llama3:latest", "qwen3:8b", "qwen3:1.7b", "deepseek-r1:1.5b"]

# 页面配置必须放在其他 st.* 调用之前，且整页只调用一次
st.set_page_config(
    page_title="AI 智能聊天",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# api_key 对本地 Ollama 无实际校验，填任意非空字符串即可
client = OpenAI(api_key="ollama", base_url=OLLAMA_BASE_URL)


def list_models() -> list[str]:
    """从 Ollama 拉取本地模型；过滤掉 embedding 模型。失败则用默认列表。"""
    try:
        names = [m.id for m in client.models.list().data]
        # nomic-embed-text 等 embedding 模型不能用于 chat
        chat_models = [n for n in names if "embed" not in n.lower()]
        return chat_models or DEFAULT_MODELS
    except Exception:
        # 常见原因：ollama 未启动 / 端口不通
        return DEFAULT_MODELS


# ---------- 侧边栏：模型选择与清空 ----------
with st.sidebar:
    st.header("设置")
    model = st.selectbox("模型", list_models(), index=0)
    if st.button("清空对话"):
        # 清空跨次重跑仍保留的消息列表，并立刻刷新页面
        st.session_state.messages = []
        st.rerun()

st.title("AI 智能聊天（本地 Ollama）")

# session_state：跨次「整页重跑」仍保留的状态字典
# 若没有它，每次输入问题后历史消息都会丢失
if "messages" not in st.session_state:
    st.session_state.messages = []  # 元素形如 {"role": "user"|"assistant", "content": "..."}

# 先回放历史消息，让聊天界面在重跑后仍完整显示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 底部聊天输入框；本轮没有新输入时直接结束，避免空跑 LLM
prompt = st.chat_input("请输入你的问题")
if not prompt:
    st.stop()

# 1) 先写入并展示用户消息
st.session_state.messages.append({"role": "user", "content": prompt})
with st.chat_message("user"):
    st.markdown(prompt)

# 2) 调用 Ollama，流式展示助手回复
with st.chat_message("assistant"):
    try:
        stream = client.chat.completions.create(
            model=model,
            # 把完整历史一并发给模型，才能多轮对话
            messages=st.session_state.messages,
            stream=True,  # 开启流式，边生成边显示
        )
        # write_stream 会逐块渲染，并返回完整拼接后的字符串
        reply = st.write_stream(chunk.choices[0].delta.content or "" for chunk in stream)
    except Exception as e:
        reply = f"调用 Ollama 失败：{e}\n\n请确认已执行 `ollama serve`，且模型已拉取。"
        st.error(reply)

# 3) 把助手回复写入历史，供下一轮重跑时回放 / 作为上下文
st.session_state.messages.append({"role": "assistant", "content": reply})
