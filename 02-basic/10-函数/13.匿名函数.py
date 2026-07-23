# 匿名函数：在函数定义时，使用 lambda 关键字定义的函数，没有函数名
# lambda 表达式：在函数定义时，使用 lambda 关键字定义的函数，没有函数名, 不能换行
add = lambda a, b: a + b
print(add(1, 2))

data_list = ["C++", "Java", "Python", "C#", "JavaScript", "Ruby", "PHP", "Go", "Swift", "Kotlin"]
data_list.sort(key=lambda x: len(x), reverse=True)
print(data_list)

# ['C#', 'C++', 'Go', 'Java', 'JavaScript', 'Kotlin', 'PHP', 'Python', 'Ruby', 'Swift']

# 匿名函数：在函数定义时，使用 lambda 关键字定义的函数，没有函数名
# 匿名函数：在函数定义时，使用 lambda 关键字定义的函数，没有函数名