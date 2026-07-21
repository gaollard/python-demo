cart = {}


while True:
    command = input("请输入命令：")
    if command == 'q':
        break
    elif command == 'add':
        item = input("请输入商品名称：")
        price = input("请输入商品价格：")
        cart[item] = price
    elif command == 'remove':
        item = input("请输入商品名称：")
        cart.pop(item)
    elif command == 'show':
        for item, price in cart.items():
            print(f"{item}: {price}")
    elif command == 'clear':
        cart.clear()
    else:
        print("命令不存在")

print(cart)