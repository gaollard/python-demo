# HTTP服务器实现
# 使用Python内置的http.server模块创建简单的HTTP服务器
import http.server
import socketserver
import socket
import os
import json
from datetime import datetime

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

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Python HTTP Server</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .container {{ max-width: 800px; margin: 0 auto; }}
                    .info {{ background: #f0f0f0; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                    .endpoint {{ background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                    code {{ background: #f5f5f5; padding: 2px 4px; border-radius: 3px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🐍 Python HTTP Server</h1>
                    <div class="info">
                        <h3>服务器信息</h3>
                        <p><strong>服务器地址:</strong> {self.server.server_address[0]}:{self.server.server_address[1]}</p>
                        <p><strong>当前时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p><strong>请求路径:</strong> {self.path}</p>
                    </div>
                    
                    <h3>可用的API端点:</h3>
                    <div class="endpoint">
                        <h4>GET /api/info</h4>
                        <p>获取服务器信息 (JSON格式)</p>
                        <code>curl http://{self.server.server_address[0]}:{self.server.server_address[1]}/api/info</code>
                    </div>
                    
                    <div class="endpoint">
                        <h4>GET /api/time</h4>
                        <p>获取当前时间</p>
                        <code>curl http://{self.server.server_address[0]}:{self.server.server_address[1]}/api/time</code>
                    </div>
                    
                    <div class="endpoint">
                        <h4>POST /api/echo</h4>
                        <p>回显POST数据</p>
                        <code>curl -X POST -d "hello world" http://{self.server.server_address[0]}:{self.server.server_address[1]}/api/echo</code>
                    </div>
                    
                    <div class="endpoint">
                        <h4>GET /files/</h4>
                        <p>浏览服务器文件目录</p>
                        <code>http://{self.server.server_address[0]}:{self.server.server_address[1]}/files/</code>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == '/api/info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            info = {
                "server": "Python HTTP Server",
                "version": "1.0",
                "host": self.server.server_address[0],
                "port": self.server.server_address[1],
                "timestamp": datetime.now().isoformat(),
                "path": self.path,
                "method": "GET"
            }
            self.wfile.write(json.dumps(info, ensure_ascii=False, indent=2).encode('utf-8'))
            
        elif self.path == '/api/time':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.wfile.write(f"当前时间: {current_time}".encode('utf-8'))
            
        elif self.path.startswith('/files/'):
            # 处理文件浏览请求
            file_path = self.path[7:]  # 移除 '/files/' 前缀
            if not file_path:
                file_path = '.'
            
            try:
                if os.path.isdir(file_path):
                    # 如果是目录，列出文件
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    
                    files = os.listdir(file_path)
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>文件列表 - {file_path}</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 40px; }}
                            .file-list {{ background: #f9f9f9; padding: 20px; border-radius: 5px; }}
                            .file-item {{ margin: 5px 0; }}
                            .directory {{ color: #0066cc; font-weight: bold; }}
                            .file {{ color: #333; }}
                        </style>
                    </head>
                    <body>
                        <h1>📁 文件列表: {file_path}</h1>
                        <div class="file-list">
                    """
                    
                    for file in sorted(files):
                        full_path = os.path.join(file_path, file)
                        if os.path.isdir(full_path):
                            html_content += f'<div class="file-item directory">📁 <a href="/files/{file}/">{file}/</a></div>'
                        else:
                            html_content += f'<div class="file-item file">📄 <a href="/files/{file}">{file}</a></div>'
                    
                    html_content += """
                        </div>
                        <p><a href="/">← 返回首页</a></p>
                    </body>
                    </html>
                    """
                    self.wfile.write(html_content.encode('utf-8'))
                else:
                    # 如果是文件，使用默认的文件服务
                    super().do_GET()
            except Exception as e:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"文件未找到: {str(e)}".encode('utf-8'))
        else:
            # 其他请求使用默认处理
            super().do_GET()
    
    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/echo':
            # 读取POST数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            response = {
                "message": "数据回显成功",
                "received_data": post_data.decode('utf-8'),
                "timestamp": datetime.now().isoformat(),
                "method": "POST"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("POST端点未找到".encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def start_server(port=8000):
    """启动HTTP服务器"""
    local_ip = get_local_ip()
    
    # 创建服务器
    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("🚀 Python HTTP Server 启动成功!")
        print("=" * 60)
        print(f"📡 服务器地址: http://{local_ip}:{port}")
        print(f"🏠 本地访问: http://localhost:{port}")
        print("=" * 60)
        print("📋 可用功能:")
        print("  • 主页: /")
        print("  • API信息: /api/info")
        print("  • 当前时间: /api/time")
        print("  • 数据回显: POST /api/echo")
        print("  • 文件浏览: /files/")
        print("=" * 60)
        print("💡 使用 Ctrl+C 停止服务器")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")

if __name__ == "__main__":
    # 可以通过命令行参数指定端口
    import sys
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ 端口号必须是数字")
            sys.exit(1)
    
    start_server(port)
