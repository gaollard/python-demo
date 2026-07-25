import requests
from bs4 import BeautifulSoup

# 定义爬取的 URL
url = "https://www.tiobe.com/tiobe-index/"

# 发送 GET 请求
response = requests.get(url)

# 打印响应内容
print(response.text)

# 解析响应内容
soup = BeautifulSoup(response.text, "html.parser")

# 打印解析后的内容
print(soup.prettify())
filename = 'tiobe.html'
with open(filename, 'w') as file_object:
    file_object.write(soup.prettify())


# 获取所有 class 为 "language-javascript" 的元素
# javascript_elements = soup.find_all(class_="language-javascript")
# print(javascript_elements)