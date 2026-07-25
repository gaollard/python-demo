`pip install requests` 和 `python -m pip install requests` 的区别


**推荐用 `python -m pip`**：它保证 pip 跟你当前这个 `python` 是同一套环境。

| | `pip install requests` | `python -m pip install requests` |
|---|---|---|
| 含义 | 直接跑名为 `pip` 的可执行文件 | 用当前 `python` 启动它自带的 pip 模块 |
| 风险 | PATH 里的 `pip` 可能指向别的 Python | 装到「你刚敲的那个 python」里 |
| 可靠性 | 多版本/虚拟环境时容易装错地方 | 更稳，官方也更推荐 |

典型踩坑：机器上有 Python 3.9 和 3.11，`pip` 绑的是 3.9，你却用 `python3.11` 跑代码 → 包装进了 3.9，`import` 却失败。

自检：

```bash
which python
which pip
python -m pip --version   # 看 pip 对应哪个 Python
```

Windows 同理，常用 `py -m pip install requests`。