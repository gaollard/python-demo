def read_lines(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:           # 文件对象本身就是惰性的
            yield line.rstrip("\n")

# 不会把整个文件读进内存
# for line in read_lines("big.txt"):
#     process(line)