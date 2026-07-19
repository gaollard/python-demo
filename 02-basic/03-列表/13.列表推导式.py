numbers = [1, 2, 3, 4, 5]

squares = [x ** 2 for x in numbers]
print(squares) # [1, 4, 9, 16, 25]

squares = [x ** 2 for x in numbers if x % 2 == 0]
print(squares) # [4, 16]