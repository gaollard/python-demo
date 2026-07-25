# 捕获任意错误：用 Exception（几乎所有运行时错误的基类）
print("Give me two numbers, and I'll divide them.")
print("Enter 'q' to quit.")

while True:
    first_number = input("\nFirst number: ")
    if first_number == 'q':
        break
    second_number = input("Second number: ")
    if second_number == 'q':
        break
    try:
        answer = int(first_number) / int(second_number)
    except Exception as e:
        # 除零、非数字等都会进这里
        print(f"出错了: {type(e).__name__} - {e}")
    else:
        print(answer)

# 说明：
# - except Exception:     捕获几乎所有“程序错误”（推荐用来兜底）
# - except:               裸 except，连 KeyboardInterrupt / SystemExit 也会捕，一般别用
# - 能明确类型时，优先写具体异常，例如 except ZeroDivisionError / ValueError
