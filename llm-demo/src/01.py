import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 1. 加载环境变量 (推荐从 .env 文件读取 API Key)
load_dotenv()

# 2. 定义提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的翻译助手，请将用户输入的内容翻译成{language}。"),
    ("human", "{text}")
])

# 3. 初始化 DeepSeek 模型
# 注意：使用 ChatOpenAI 类，但配置 DeepSeek 的 API 地址和密钥
llm = ChatOpenAI(
    model="deepseek-chat",  # 或 "deepseek-v4-flash"
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.7
)

# 4. 定义输出解析器
output_parser = StrOutputParser()

# 5. 使用 | 操作符将组件串联成链
chain = prompt | llm | output_parser

# 6. 调用链并获取结果
result = chain.invoke({"language": "中文", "text": "Hello, LangChain!"})
print(result)
# 预期输出: 你好，LangChain！