import asyncio

async def hello(name: str) -> str:
    await asyncio.sleep(0.1)
    return f"hello, {name}"

async def main():
    msg = await hello("Ada")
    print(msg)              # hello, Ada

asyncio.run(main())         # 程序入口：创建并跑完事件循环