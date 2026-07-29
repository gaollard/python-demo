# llm-demo

LangChain 最小示例：用提示词模板 + 模型 + 输出解析器组成一条调用链。

## 依赖说明

### `langchain_core`

LangChain 的**核心抽象层**，与具体厂商无关。提供可组合的基础组件：

| 组件 | 作用 | 本仓库用法 |
|------|------|------------|
| `ChatPromptTemplate` | 把 system / human 消息写成带变量的模板 | `from_messages([...])`，占位符如 `{language}` |
| `StrOutputParser` | 把模型返回的消息对象解析成纯字符串 | 链尾 `| output_parser` |
| LCEL（`\|` 管道） | 把 Prompt → LLM → Parser 串成一条链 | `chain = prompt \| llm \| output_parser` |

特点：只定义「怎么拼链路」，不负责真正调哪个云厂商的 API。

### `langchain_openai`

LangChain 的 **OpenAI 兼容接口适配包**。提供 `ChatOpenAI` 等实现，底层走 OpenAI SDK 协议。

本仓库用它对接 DeepSeek（兼容 OpenAI API）：

```python
ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
)
```

特点：负责「真正发起 HTTP 请求、收模型回复」；只要服务端兼容 OpenAI Chat Completions，就能复用同一套类。

## 二者关系

```
langchain_core          →  抽象：Prompt / Parser / Chain
langchain_openai        →  实现：ChatOpenAI（可指向 OpenAI / DeepSeek 等）
```

典型流水线：`prompt`（core）→ `llm`（openai 包）→ `output_parser`（core）。
