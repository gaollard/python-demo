str = "hello world"
print(str.split())
print(str.split(' '))
print(str.split('o'))

def split_string(str, delimiter):
    return str.split(delimiter)

print(split_string("hello world", " "))
print(split_string("hello world", "o"))
print(split_string("hello world", "l"))
print(split_string("hello world", "h"))
print(split_string("hello world", "w"))
print(split_string("hello world", "r"))
print(split_string("hello world", "d"))
print(split_string("hello world", "e"))
print(split_string("hello world", "f"))