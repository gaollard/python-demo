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

pip freeze > requirements.txt 命令主要用于将当前 Python 环境中已安装的所有第三方包及其精确版本号，导出并保存到一个名为 requirements.txt 的文本文件中。

这个文件在 Python 项目开发中扮演着重要角色。它详细记录了项目运行所依赖的库及其特定版本，例如 Django==4.2.7
1。当其他人获取你的项目代码，或者在新的环境（如部署服务器、另一台开发机）中需要配置项目时，只需运行 pip install -r requirements.txt 命令，就能一键安装文件中列出的所有依赖包，从而快速复现出与开发时一致的运行环境
2。

通过这种方式，requirements.txt 文件有效保证了项目在不同环境下的依赖一致性，避免了因库版本不同可能导致的各种问题，极大提升了项目协作和部署的效率

## 后台运行
1. 使用&在Unix-like系统（如Linux或MacOS）
在命令行中，你可以通过在命令末尾添加&来将Python脚本放到后台运行。例如：

```
python your_script.py &
```

2. 使用nohup命令
nohup命令可以在Unix-like系统中用于运行命令，使得该命令在用户注销后仍然继续运行。例如：
```
nohup python your_script.py &
```
这样即使你关闭了终端，脚本也会继续运行。nohup命令的输出默认会重定向到nohup.out文件中。

4. 使用Python的subprocess模块
如果你希望在Python脚本内部启动另一个Python脚本或任何其他程序，可以使用subprocess模块。例如：

```python
import subprocess

subprocess.Popen(['python', 'your_script.py'])
```

这会以子进程的方式启动你的脚本，并且父进程可以继续执行。

## 作用域
在Python中，只有模块（module）、函数（def）和类（class）会创建新的作用域。if、for、while等流程控制语句不会创建独立的作用域，在其中定义的变量属于其所在的作用域（通常是函数作用域或全局作用域）。