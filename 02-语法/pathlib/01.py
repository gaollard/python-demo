from pathlib import Path

path = Path(__file__).parent / "data" / "out.txt"
print(path.name)      # out.txt
print(path.stem)      # out
print(path.suffix)    # .txt
print(path.parent)    # /tmp/project/data

path.write_text(
    "hello",
    encoding="utf-8"
)
print(path.read_text(encoding="utf-8"))  # hello