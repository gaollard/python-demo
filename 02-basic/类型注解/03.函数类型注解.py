# args 位置参数，类型注解
# *args: T 表示「每一个」传入的位置参数都是类型 T，而不是整个 args 是 T
def getProductPrice(buyer_name, *args: tuple[str, float | int, int]):
    """
    :param args: 每个参数都是商品信息 ("苹果", 200, 2) => 名称，价格，数量
    """
    print(buyer_name, *args)
    # args 形如: (("苹果", 200, 2),)
    name, price, count = args[0]
    return price * count


# 正确调用：传入一个 tuple，而不是三个散开的参数
print(getProductPrice("Frank", ("苹果", 200, 2)))

# 也可以一次传多个商品
# print(getProductPrice(("苹果", 200, 2), ("香蕉", 100, 3)))


# 如果只想传名称、价格、数量三个散开参数，不要用 *args 包成「tuple 类型」，
# 直接给每个形参做注解即可：
def getProductPrice2(name: str, price: float | int, count: int) -> float | int:
    return price * count

print(getProductPrice2("苹果", 200, 2))

def getProductPrice3(name: str, *args: str, **kwargs: str):
    """
    返回姓名、朋友列表和其他信息

    :param name: 姓名
    :param args: 不定长位置参数，朋友名称，如 "朋友1", "朋友2"
    :param kwargs: 不定长关键字参数，其他信息，如 city="北京", phone="18888888888"
    :return: (姓名, 朋友元组, 其他信息字典)
    """
    return name, args, kwargs

print(getProductPrice3("Frank", "朋友1", "朋友2", city="北京", phone="18888888888"))

# 位置参数 和 关键字参数 可以混合使用
# 位置参数 必须放在 关键字参数 前面