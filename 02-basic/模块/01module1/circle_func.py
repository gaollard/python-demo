value = 0

# 根据圆半径计算圆的面积
def circle_area(radius: float) -> float:
    return 3.14 * radius ** 2

# 根据圆半径计算圆的周长
def circle_perimeter(radius: float) -> float:
    return 2 * 3.14 * radius

# 根据圆半径计算圆的直径
def circle_diameter(radius: float) -> float:
    return 2 * radius

def define_val():
    global age
    age = 10

def update_val():
    global value
    value = 1