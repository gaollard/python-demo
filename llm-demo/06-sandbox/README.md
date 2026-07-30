沙箱内不能读取沙箱外


因为沙箱只包住了 shell，没有包住整个 agent。

这里其实是两条通路：

通路	跑在哪	能不能读 README
shell（ShellToolMiddleware）
workspace/ 里的 shell 会话
按设计不行（README 在 workspace 外）
read_readme（普通 @tool）
宿主 Python 进程
可以，Path.read_text() 直接读本机文件
ShellToolMiddleware(workspace_root=WORKSPACE) 只限制 shell 命令的工作目录；read_readme 是你自己注册的 tool，在 agent 进程里执行，不走沙箱：