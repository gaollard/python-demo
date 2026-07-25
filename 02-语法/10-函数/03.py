def count_alpha(text):
    """
    统计文本中字母的个数和字母的组合
    :param text: 文本
    :return: 字母的个数和字母的组合
    """
    count = 0
    str = ""
    for char in text:
        if char.isalpha():
            count += 1
            str += char
    return count, str

count, str = count_alpha("Hello, World!")
print(count)
print(str)


# 给定一个字符串，统计元音字母的个数
def count_vowel(text):
    """
    统计文本中元音字母的个数
    :param text: 文本
    :return: 元音字母的个数
    """
    count = 0
    str = ""
    for char in text:
        if char.lower() in "aeiou":
            count += 1
            str += char
    return count, str

print(count_vowel("Hello, World!"))

# 给定一个分数列表，统计最高分 最低分 和平均分
def count_score(scores):
    """
    统计分数列表中最高分 最低分 和平均分
    :param scores: 分数列表
    :return: 最高分 最低分 和平均分
    """
    max_score = max(scores)
    min_score = min(scores)
    average_score = sum(scores) / len(scores)
    return max_score, min_score, average_score

print(count_score([100, 90, 80, 70, 60]))