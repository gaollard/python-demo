# *args：不定长参数，可以传入任意个参数
# **kwargs：不定长参数，可以传入任意个关键字参数
def print_person(name, age, *args, **kwargs):
    """
    打印个人信息
    :param name: 姓名
    :param age: 年龄
    :param args: 不定长参数
    :param kwargs: 不定长关键字参数
    """
    print(f"name: {name}")
    print(f"age: {age}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

print_person("张三", 18, "男", "北京", "18888888888", city="北京", phone="18888888888")

# name: 张三
# age: 18
# args: ('男', '北京', '18888888888')
# kwargs: {'city': '北京', 'phone': '18888888888'}

# 不定长参数：在函数定义时，给参数设置不定长参数，在函数调用时，可以传入任意个参数
# 不定长参数必须放在位置参数后面
# 不定长参数必须放在位置参数后面


def calc_sum(*args):
    print(f"len(args): {len(args)}")
    return sum(args)

print(calc_sum(1, 2, 3, 4, 5))

# 15

def calc_sum(**kwargs):
    print(f"len(kwargs): {len(kwargs)}")
    return sum(kwargs.values())

print(calc_sum(a=1, b=2, c=3))