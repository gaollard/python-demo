import utils.circle_func as circle
import utils.my_fun as my_fun
from utils.circle_func import circle_area

print(circle.circle_area(10))
my_fun.say_hello()
my_fun.say_goodbye()

print(circle_area(10))

from core.db.connect import db_connect
print(db_connect())

# logger 目录不是包，不能直接导入
from core.logger.console import log
log("test")