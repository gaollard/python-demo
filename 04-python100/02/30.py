# 简易登录：验证用户名和密码是否匹配预设值。

pwd="123456"
username="admin"

_pwd=input("请输入密码：")
_username=input("请输入用户名：")

if _pwd==pwd and _username==username:
    print("登录成功！")
else:
    print("用户名或密码错误。")