list1 = [1, 2, 3]
list2 = [4, 5, 6]

list3 = list1 + list2

print(list3) # [1, 2, 3, 4, 5, 6]
print(type(list3))

print([*list1, *list2]) # [1, 2, 3, 4, 5, 6]
print(type([*list1, *list2]))