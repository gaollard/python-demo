# 货币转换器：人民币与美元按固定汇率互相转换。

value = float(input("请输入人民币金额："))

rmb_to_usd = 8

def cal(rmbValue):
    return round(rmbValue / rmb_to_usd, 2)

print("人民币", value, "元转换为美元为：", cal(value), "美元")