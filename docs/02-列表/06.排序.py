bicycles = ['js','world','world','java','c','c++']

bicycles.sort()
print(bicycles)

bicycles.sort(reverse=True)
print(bicycles)

# 按长度排序
bicycles.sort(key=len)
print(bicycles)

# bicycles.sort(key=len, reverse=True)
# print(bicycles)

# 临时排序
print(sorted(bicycles))
print(bicycles)