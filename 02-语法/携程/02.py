import asyncio

async def fetch(name: str) -> str:
    print(f"fetching {name}")
    await asyncio.sleep(1)  # 可等待的「假睡眠」，会让出控制权
    return f"data-{name}"

async def main():
    a, b = await asyncio.gather(fetch("A"), fetch("B"))
    print(a, b)             # 总共约 1 秒

asyncio.run(main())