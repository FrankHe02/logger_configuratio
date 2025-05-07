import logging
import threading
from logger_config import setup_root_logger, setup_thread_logger
from common_module import common_function
from common_module1 import common_function as common_function1
from logger_thread_utils import thread_local

LOG_FILE_PATH = 'logs/中文/中文_特殊￥_/thread_'


def thread_function(thread_id, log_file_path=None):
    # 为当前线程设置日志记录器到线程局部存储
    thread_local.logger = setup_thread_logger(thread_id, log_file_path)
    logger = thread_local.logger
    for i in range(3000):
        common_function()
        common_function1()
        logger.info(f'Thread {thread_id} is in iteration {i}')


if __name__ == "__main__":
    # 配置根日志记录器
    setup_root_logger()

    # 直接使用 logging 模块，实际上使用的是根日志记录器
    logging.debug('This is a debug message from the main module')
    logging.info('This is an info message from the main module')

    num_threads = 3
    threads = []

    for i in range(num_threads):
        # 可根据需要指定日志文件路径
        log_file_path = f'{LOG_FILE_PATH}{i}'
        # 创建线程实例
        thread = threading.Thread(target=thread_function, args=(i, log_file_path))
        threads.append(thread)
        # 启动线程
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    print("All threads have completed.")
