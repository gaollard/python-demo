age = 12
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

age = 70

if age >= 18 and age < 65:
    print("You are an adult")
elif age >= 65:
    print("You are a senior")
else:
    print("You are a minor")


if age < 4:
    print("Your admission cost is $0.")
elif age < 18:
    print("Your admission cost is $5.")
else:
    print("Your admission cost is $10.")

age = 12
if age in [12, 20]:
    print("You are a teenager")
else:
    print("You are not a teenager")