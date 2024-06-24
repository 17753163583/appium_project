import traceback
from datetime import datetime
from functools import wraps
from pathlib import Path

from loguru import logger

# 日志目录的创建
log_dir = Path(__file__).resolve().parent.parent.joinpath("logs")

if not log_dir.exists() or not log_dir.is_dir():
    try:
        log_dir.mkdir(parents=True)
    except PermissionError:
        logger.error("没有权限创建日志目录")
    except Exception as e:
        logger.error(f"创建日志目录时发生错误: {e}")

# "%y-%m-%d_%H-M-%S"
current_time = datetime.now().strftime("%Y-%m-%d")
log_name = f"log_{current_time}.log"

log_file_path = log_dir.joinpath(log_name)
logger.add(
    log_file_path, rotation="1 week", retention="1 month", level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}", enqueue=True,
    backtrace=True,
    diagnose=True, encoding="utf-8")


def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        包装器函数，实际执行被装饰函数，并记录相关日志。
        参数:
        - *args: 位置参数。
        - **kwargs: 关键字参数。
        返回值:
        - 被装饰函数的返回值。
        """
        # 记录函数开始执行的日志
        logger.info(f"函数 {func.__name__} 开始执行，入参:{args}{kwargs}")
        try:
            # 尝试执行函数
            result = func(*args, **kwargs)
            # 记录函数执行成功及返回结果的日志
            logger.info(f"函数 {func.__name__} 执行完成，函数返回结果：{result}\n")
            return result
        except Exception:
            # 记录函数执行失败的错误日志
            exception_traceback = traceback.format_exc()
            logger.error(f"函数 {func.__name__} 异常堆栈：{exception_traceback}\n")

    return wrapper
