import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()


@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    print(f"search_database: Searching the database for '{query}'")
    return f"Found {limit} results for '{query}'"


# 字符串 "deepseek-chat" 会走 ChatDeepSeek，需额外安装 langchain-deepseek。
# 这里直接传入 ChatOpenAI，与 01 示例一致，复用 OpenAI 兼容协议对接 DeepSeek。
llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_base="https://api.deepseek.com/v1",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0.3,
)

agent = create_agent(model=llm, tools=[search_database])
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Search the database for customer Alice, return the results in JSON format"
            }
        ]
    }
)

print(type(response))  # <class 'dict'>
print(response.keys())  # dict_keys(['messages'])
# 最终回复在最后一条 AIMessage 里
print(response["messages"][-1].content)