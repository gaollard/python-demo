01 如何执行 python 程序
02 参考手册 https://docs.python.org/zh-cn/3.13/tutorial/index.html
03 python 并发模型 https://zhuanlan.zhihu.com/p/354982602
04 Django https://docs.djangoproject.com/en/5.2/
05 requirements.txt 依赖管理 
06 fast

Python提供了三种并发的工具：多线程（threading）、多进程（process）和协程（Coroutine）。前两种其实就是利用了操作系统提供的并发模型。

## 依赖生成

```sh
pip freeze > requirements.txt
```

pip freeze > requirements.txt 命令主要用于将当前 Python 环境中已安装的所有第三方包及其精确版本号，导出并保存到一个名为 requirements.txt 的文本文件中