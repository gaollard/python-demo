import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1. 加载环境变量 (推荐从 .env 文件读取 API Key)
load_dotenv()

# 2. 定义提示词模板：让大模型写节流函数
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一名资深前端工程师。请用 {language} 编写代码，"
        "只输出完整可运行的函数与简短用法示例，不要额外寒暄。",
    ),
    (
        "human",
        "请实现一个节流函数 throttle，要求：\n"
        "1. 签名：throttle(fn, wait)\n"
        "2. 在 wait 毫秒内，无论触发多少次，最多执行一次 fn\n"
        "3. 保留第一次触发时的 this 与参数\n"
        "4. 返回的包装函数可正常调用\n"
        "语言环境补充：{extra}",
    ),
])

# 3. 初始化 DeepSeek 模型
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

# 4. 定义输出解析器
output_parser = StrOutputParser()

# 5. 使用 | 操作符将组件串联成链
chain = prompt | llm | output_parser

# 6. 调用链并获取结果
result = chain.invoke({
    "language": "JavaScript",
    "extra": "ES6+，不要依赖第三方库",
})
print(result)
