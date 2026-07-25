print("读取文件")
with open('pi_digits.txt') as file_object:
    contents = file_object.read()
    print(contents)

print("逐行读取文件")
with open('pi_digits.txt') as file_object:
    for line in file_object:
        print(line)

print("将文件内容存储到列表中")
print("\nReading in the entire file:")
with open('pi_digits.txt') as file_object:
    lines = file_object.readlines()
    for line in lines:
        print(line)