# BMI 计算器：输入身高体重，计算 BMI 并给出健康建议。

height = float(input("请输入身高（米）："))
weight = float(input("请输入体重（公斤）："))

# BMI = 体重(kg) ÷ 身高(m)²

bmi = weight / (height ** 2)

print(f"您的 BMI 为: {bmi:.2f}")