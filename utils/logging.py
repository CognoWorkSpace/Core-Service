"""
usage description:
use python row logging module
supported four level: INFO, WARNING, ERROR, CRITICAL, you can use these four level info to record log due to different
situation and you can find this log file in current project dir when running this app, the path will be changed through
config.yml

code example:
from logger import LOGGER
error = "123"
LOGGER.error("Print ERROR level log, error is {}".format(error))
LOGGER.warning("Print WARNING level log")
LOGGER.info("Print INFO level log")

display:

2023-07-17 05:49:50,674 - ERROR - demo.py - <module> - 3 - Print ERROR level log, error is 123
2023-07-17 05:49:50,674 - WARNING - demo.py - <module> - 4 - Print WARNING level log
2023-07-17 05:49:50,674 - INFO - demo.py - <module> - 5 - Print INFO level log

as the first log as example
2023-07-17 05:49:50,674 -> logging time
ERROR -> logging level
demo.py -> use log  file location
<module> -> which function use
3 -> logging write line in this file
Print ERROR level log, error is 123 -> message
"""
import logging
import os

# 1. Create a logger instance, and name the logger instance as "single info", the set severity level is DEBUG
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

# 2. Create a handler, this is mainly used to output logs to the console, and set the severity level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 3. Create the output format (formatter) for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')

# 4. Add formatter to handler
ch.setFormatter(formatter)

# rHandler = logging.FileHandler('/Users/15408/PycharmProjects/Core-Service/logs'+'/'+os.environ['FLASK_ENV']+'.log', encoding="utf-8", mode="a")
rHandler = logging.FileHandler('./logs/'+os.environ['FLASK_ENV']+'.log', encoding="utf-8", mode="a")
rHandler.setLevel(logging.INFO)
rHandler.setFormatter(formatter)
# 5.将handler添加到logger中
LOGGER.addHandler(ch)
LOGGER.addHandler(rHandler)

