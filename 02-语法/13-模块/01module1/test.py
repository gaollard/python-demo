# 用法1
# import core.logger as logger

# logger.log("test")
# logger.info("test")
# logger.warning("test")
# logger.error("test")
# logger.critical("test")

# 用法2
from core.logger import log, info, warning, error, critical

log("test")
info("test")
warning("test")
error("test")
critical("test")