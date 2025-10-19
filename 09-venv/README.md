安装 Django
```shell
./ll_env/bin/python -m pip install Django
```

创建项目
```shell
 ./ll_env/bin/django-admin startproject hello_world .
```

启动服务
```shell
 ./ll_env/bin/python manage.py runserver 
```

```shell
python manage.py startapp polls
```

应用目录
```
app_name/
  ├── migrations/       # 数据库迁移文件
  ├── __init__.py
  ├── admin.py         # 管理后台配置
  ├── apps.py          # 应用配置
  ├── models.py        # 数据模型
  ├── tests.py         # 测试用例
  └── views.py         # 视图函数
```