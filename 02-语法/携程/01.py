import time

def fetch_sync(name: str) -> str:
    time.sleep(1)          # 模拟网络 I/O
    return f"data-{name}"

def main():
    a = fetch_sync("A")
    b = fetch_sync("B")
    print(a, b)            # 总共约 2 秒

main()