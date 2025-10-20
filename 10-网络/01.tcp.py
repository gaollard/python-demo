# 获取本地主机IP地址
import socket

# 原始问题： socket.gaierror: [Errno 8] nodename nor servname provided, or not known
# 原因： socket.gethostname() 在某些系统配置下可能返回无法解析的主机名，导致 socket.gethostbyname() 失败。
# 解决方案： 我实现了一个更可靠的 get_local_ip() 函数，使用了三种备用方法：
# 主要方法： 通过连接外部地址（8.8.8.8）获取本机IP
# 备用方法1： 使用原始的主机名解析方法
# 备用方法2： 如果都失败，返回 localhost (127.0.0.1)
# 测试结果： 代码现在可以正常运行，成功获取到本机IP地址 10.53.100.31 和主机名 C02G211KMD6M。
# 这种方法更加健壮，能够在各种网络环境下正常工作。

def get_local_ip():
    """获取本机IP地址的可靠方法"""
    try:
        # 方法1: 通过连接外部地址获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        try:
            # 方法2: 通过主机名获取
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            return local_ip
        except Exception:
            # 方法3: 使用localhost
            return "127.0.0.1"

local_ip = get_local_ip()
print(f"本机IP地址: {local_ip}")

# 显示主机名信息
try:
    hostname = socket.gethostname()
    print(f"主机名: {hostname}")
except Exception as e:
    print(f"无法获取主机名: {e}")