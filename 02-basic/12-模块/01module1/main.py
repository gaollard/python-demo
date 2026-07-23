from circle_func import circle_area, circle_perimeter, circle_diameter, define_val, update_val
from circle_func import value
import circle_func

# print(circle_area(10))
# print(circle_perimeter(10))
# print(circle_diameter(10))

print(value) # 0
update_val()
print(value) # 为什么这里还是 0 ?
print(circle_func.value) # 1

# 非常关键的一点：
"""
在 Python 中，import 语句是按值拷贝的。也就是说，当你执行 import circle_func 时，
你拿到的 value 值，是 circle_func 模块里 value 变量在那一刻的值。
"""

print(circle_func.age) # AttributeError: module 'circle_func' has no attribute 'age'
define_val()
print(circle_func.age) # 10