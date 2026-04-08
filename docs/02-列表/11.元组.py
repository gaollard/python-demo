# 不可变的列表称为元组
dimensions = (200,50)
print(dimensions[0])
print(dimensions[1])

# dimensions[0] = 250
# print(dimensions[0])

for dimension in dimensions:
    print(dimension)

dimensions = (400,100)
print(dimensions)