bicycles = ['JS','world','python','java','c','c++']
print(bicycles)
print(bicycles[0])
print(bicycles[1])
print(bicycles[-1]) # 最后一个元素
print(bicycles[-2]) # 倒数第二个元素

# 修改列表中的元素
bicycles[0] = 'hello'
print(bicycles)


bicycles.append('php')
print(bicycles)

bicycles.insert(0, 'html')
print(bicycles)

# 删除末尾元素
bicycles.pop()
print(bicycles)

# 删除指定位置的元素
bicycles.pop(0)
print(bicycles)