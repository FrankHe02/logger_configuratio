import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


# 全局通用参数定义
DEFAULT_MAX_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_BACKUP_COUNT = 5
DEFAULT_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def generate_log_filename(prefix):
    """
    生成包含时间戳的日志文件名。
    :param prefix: 日志文件前缀
    :return: 生成的日志文件名
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{timestamp}.log"


def create_log_directory(log_file):
    """
    检查日志文件所在目录是否存在，若不存在则创建。
    :param log_file: 日志文件路径
    """
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, exist_ok=True)
        except Exception as e:
            logging.error(f"Failed to create log directory {log_dir}: {e}")


def create_file_handler(log_file, max_size=DEFAULT_MAX_SIZE, backup_count=DEFAULT_BACKUP_COUNT, level=logging.DEBUG):
    """
    创建 RotatingFileHandler 用于按文件大小切片存储日志。
    :param log_file: 日志文件路径
    :param max_size: 单个日志文件的最大大小，单位为字节
    :param backup_count: 保留的旧日志文件数量
    :param level: 日志处理器的日志级别
    :return: 配置好的 RotatingFileHandler
    """
    file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
    file_handler.setLevel(level)
    return file_handler


def create_console_handler(level=logging.DEBUG):
    """
    创建控制台处理器，将日志输出到控制台。
    :param level: 日志处理器的日志级别
    :return: 配置好的 StreamHandler
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    return console_handler


def setup_root_logger(log_file_prefix='app', max_size=DEFAULT_MAX_SIZE, backup_count=DEFAULT_BACKUP_COUNT):
    """
    配置根日志记录器，支持按文件大小切片存储日志，文件名包含时间戳。
    :param log_file_prefix: 根日志文件的前缀
    :param max_size: 单个日志文件的最大大小，单位为字节，默认为 10MB
    :param backup_count: 保留的旧日志文件数量，默认为 5 个
    """
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 生成日志文件名
    log_file = generate_log_filename(log_file_prefix)

    # 创建日志目录
    create_log_directory(log_file)

    # 创建文件处理器
    file_handler = create_file_handler(log_file, max_size, backup_count)

    # 创建控制台处理器
    console_handler = create_console_handler()

    # 使用全局格式
    file_handler.setFormatter(DEFAULT_FORMATTER)
    console_handler.setFormatter(DEFAULT_FORMATTER)

    # 将处理器添加到根日志记录器
    try:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    except Exception as e:
        logging.error(f"Failed to add handlers to root logger: {e}")


def setup_thread_logger(thread_id, log_file_prefix=None, max_size=DEFAULT_MAX_SIZE, backup_count=DEFAULT_BACKUP_COUNT):
    """
    为线程配置专属的日志记录器，支持按文件大小切片存储日志，文件名包含时间戳。
    :param thread_id: 线程的编号
    :param log_file_prefix: 线程日志文件的前缀，若未指定则使用默认前缀
    :param max_size: 单个日志文件的最大大小，单位为字节，默认为 10MB
    :param backup_count: 保留的旧日志文件数量，默认为 5 个
    :return: 配置好的线程日志记录器
    """
    # 创建线程专属的日志记录器
    logger = logging.getLogger(f'thread_{thread_id}')
    logger.setLevel(logging.DEBUG)

    # 若未指定日志文件前缀，则使用默认前缀
    if log_file_prefix is None:
        log_file_prefix = f'thread_{thread_id}'

    # 生成日志文件名
    log_file = generate_log_filename(log_file_prefix)

    # 创建日志目录
    create_log_directory(log_file)

    # 检查日志记录器是否已有对应的处理器，避免重复添加
    for handler in logger.handlers:
        if isinstance(handler, RotatingFileHandler) and handler.baseFilename == os.path.abspath(log_file):
            return logger

    # 创建文件处理器
    file_handler = create_file_handler(log_file, max_size, backup_count)

    # 使用全局格式
    file_handler.setFormatter(DEFAULT_FORMATTER)

    # 将处理器添加到线程日志记录器
    try:
        logger.addHandler(file_handler)
    except Exception as e:
        logging.error(f"Failed to add handler to thread logger {logger.name}: {e}")

    return logger
