class DemoCM:
    def __enter__(self):
        print("enter")
        return "资源对象"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit", exc_type)
        return False   # False / None：不吞掉异常；True：抑制异常

with DemoCM() as value:
    print("body:", value)

# - 返回 `False` / `None`：异常继续传播（默认行为）
# - 返回 `True`：抑制异常，`with` 之后的代码继续执行