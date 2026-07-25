from contextlib import closing
import urllib.request

# 对于只有 close() 方法的对象，可以直接使用：
with closing(urllib.request.urlopen('https://example.com')) as page:
    html = page.read()