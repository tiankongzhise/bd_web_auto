import logging
import logging.config
import os 

config_path = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
#读取日志配置文件
logging.config.fileConfig(config_path)

#获取日志记录器
logger = logging.getLogger()

