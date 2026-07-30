"""Sandbox 示例：用 ShellToolMiddleware 给 agent 提供受控 shell 执行环境。

对比 05：05 用 subprocess 跑白名单脚本；这里让 agent 通过 shell 工具在
独立 workspace 里执行命令，并用 execution_policy 限制超时与输出。

隔离强度由 policy 决定：
- HostExecutionPolicy：本机进程，限制超时/输出（本示例，零额外依赖）
- DockerExecutionPolicy：容器隔离（需 Docker，适合更强安全边界）
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import (
    HostExecutionPolicy,
    ShellToolMiddleware,
)
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

DEMO_DIR = Path(__file__).resolve().parent
README_PATH = DEMO_DIR / "README.md"
WORKSPACE = DEMO_DIR / "workspace"
WORKSPACE.mkdir(exist_ok=True)


@tool
def read_readme() -> str:
    """读取本示例目录下的 README.md（位于沙箱工作区之外）。

    shell 只能访问 workspace；要用此工具读取沙箱外的 README。
    """
    print(f"[tool] read_readme() -> {README_PATH}")
    if not README_PATH.is_file():
        return f"README not found: {README_PATH}"
    body = README_PATH.read_text(encoding="utf-8")
    # 明确标注为文件正文，避免模型把 README 内容误当成工具报错
    return (
        f"OK: read {README_PATH.name} successfully (path outside sandbox).\n"
        f"----- BEGIN README.md -----\n"
        f"{body.rstrip()}\n"
        f"----- END README.md -----"
    )

llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.2,
)

# 本机执行 + 超时/输出上限。若本机有 Docker，可换成：
# from langchain.agents.middleware import DockerExecutionPolicy
# execution_policy = DockerExecutionPolicy(network_enabled=False, ...)
execution_policy = HostExecutionPolicy(
    command_timeout=30.0,
    max_output_lines=200,
)

shell_middleware = ShellToolMiddleware(
    workspace_root=WORKSPACE,
    execution_policy=execution_policy,
    env={
        # 最小环境，避免把 API Key 等宿主变量带进 shell
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": str(WORKSPACE),
        "LANG": "C.UTF-8",
    },
)

SYSTEM = """你是代码助手，可以通过 shell 在沙箱工作区执行命令，也可用 read_readme 读示例说明。

## 规则
1. 需要计算、读工作区内文件、跑 Python 时，优先调用 shell
2. shell 只在当前工作目录内操作；不要用 shell 访问工作区外路径
3. 需要了解本示例说明（README.md）时，调用 read_readme（该文件在沙箱外）
4. 用 python3 -c 或临时 .py 文件完成计算，把 stdout 作为依据回答
5. shell 的 stdout 必须以换行结尾（LangChain ShellSession 坑：无 \\n 会卡到超时）。
   写文件用 print(..., file=f) 或 f.write(text + "\\n")；读文件用 echo "$(cat f)" 或 cat f; echo
6. 回复使用简体中文
"""

agent = create_agent(
    model=llm,
    tools=[read_readme],  # shell 由 middleware 注册
    middleware=[shell_middleware],
    system_prompt=SYSTEM,
)

USER_QUERY = (
    "先用工具读一下 README，告诉我里面写了什么；"
    "然后在工作区用 Python 计算 1 到 100 的和，并把结果写入 sum.txt（末尾带换行），"
    "最后读出该文件内容告诉我。"
)

print(f"workspace: {WORKSPACE}")
print(f"execution_policy: {type(execution_policy).__name__}")
print("=" * 60)

response = agent.invoke({"messages": [{"role": "user", "content": USER_QUERY}]})

print("最终回复:")
print(response["messages"][-1].content)
print("=" * 60)

for msg in response["messages"]:
    if getattr(msg, "tool_calls", None):
        for call in msg.tool_calls:
            print(f"tool_call -> {call['name']}({call.get('args', {})})")
