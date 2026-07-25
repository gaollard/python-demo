def sleep():
    print("sleep called")
    return {"Hello": "World"}

print(sleep.__name__); # 输出 sleep 

result = sleep()
print(result)