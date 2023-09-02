"""
usage description:
use python row logging module
supported four level: INFO, WARNING, ERROR, CRITICAL, you can use these four level info to record log due to different
situation and you can find this log file in current project dir when running this app, the path will be changed through
config.yml

code example:
from logger import LOGGER
error = "123"
LOGGER.error("打印ERROR级别日志, error is {}".format(error))
LOGGER.warning("打印WARNING级别日志")
LOGGER.info("打印INFO级别日志")

display:

2023-07-17 05:49:50,674 - ERROR - demo.py - <module> - 3 - 打印ERROR级别日志, error is 123
2023-07-17 05:49:50,674 - WARNING - demo.py - <module> - 4 - 打印WARNING级别日志
2023-07-17 05:49:50,674 - INFO - demo.py - <module> - 5 - 打印INFO级别日志

as the first log as example
2023-07-17 05:49:50,674 -> logging time
ERROR -> logging level
demo.py -> use log  file location
<module> -> which function use
3 -> logging write line in this file
打印ERROR级别日志, error is 123 -> message
"""
import logging

# 1.创建一个logger实例，并且logger实例的名称命名为“single info”，设定的严重级别为DEBUG
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

# 2.创建一个handler，这个主要用于控制台输出日志，并且设定严重级别
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 3.创建handler的输出格式（formatter）
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')

# 4.将formatter添加到handler中
ch.setFormatter(formatter)

rHandler = logging.FileHandler('test.log', encoding="utf-8", mode="a")
rHandler.setLevel(logging.INFO)
rHandler.setFormatter(formatter)
# 5.将handler添加到logger中
LOGGER.addHandler(ch)
LOGGER.addHandler(rHandler)

