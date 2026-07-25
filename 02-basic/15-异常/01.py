# try:
#     print(my_name)
# except ZeroDivisionError: # 无法捕获未定义的变量
#     print("NameError: name 'my_name' is not defined")

# try:
#     print(my_name)
# except NameError as e: # 能捕获
#     print(f"变量未定义: {e}")

try:
    print(my_name)
except ZeroDivisionError as e: # 能捕获
    print(f"ZeroDivisionError: {e}")
except NameError as e: # 能捕获
    print(f"NameError: {e}")