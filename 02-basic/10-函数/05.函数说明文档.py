# 定义一个函数，计算圆的面积
def circle_area(radius):
    """
    计算圆的面积
    :param radius: 圆的半径
    :return: 圆的面积
    """

    return 3.14 * radius * radius

print(f"circle_area.__doc__: {circle_area.__doc__}")
print(f"circle_area.__name__: {circle_area.__name__}")
print(f"circle_area.__module__: {circle_area.__module__}")
print(f"circle_area.__defaults__: {circle_area.__defaults__}")
print(f"circle_area.__code__: {circle_area.__code__}")
print(f"circle_area.__closure__: {circle_area.__closure__}")
print(f"circle_area.__dict__: {circle_area.__dict__}")

help(circle_area)
