import logging
from logger_config import setup_root_logger
from logger_thread_utils import thread_local

# 检查是否为单独运行该模块，如果是则配置根日志记录器
if __name__ == "__main__":
    setup_root_logger()


def common_function():
    # 尝试从线程局部存储获取当前线程的日志记录器
    logger = getattr(thread_local, 'logger', logging.getLogger())
    logger.critical('This is a critical message from the common module1')
    logger.error('This is a error message from the common module1')
    logger.warning('This is a warning message from the common module1')
    logger.debug('This is a debug message from the common module1')
    logger.info('This is an info message from the common module1')


# 用于单独调试
if __name__ == "__main__":
    common_function()
