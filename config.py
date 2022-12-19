import os
import logging
from logging.handlers import TimedRotatingFileHandler

# link to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///bonfire.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Key information
SECRET_KEY = "CGBHGCYTGYIHUONHGVTGYHUBHJG"

# mail server
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "2964992240@qq.com"
MAIL_PASSWORD = "lvnbpinsuqcvdgcb"
MAIL_DEFAULT_SENDER = "2964992240@qq.com"

AVATAR_UPLOAD_FOLDER = "static/upload/avatar/"
BACKGROUND_UPLOAD_FOLDER = "static/upload/background/"
POST_UPLOAD_FOLDER = "static/upload/posts_images/"

LOG_FILE_BASE = ["log/DEBUG/", "log/INFO/"]
for log_file in LOG_FILE_BASE:
    if not os.path.exists(log_file):
        os.makedirs(log_file)


def init_log(log_name):
    """
    初始化日志
    :return:
    """
    if log_name == "DEBUG":
        log_level = logging.DEBUG
        LOG_FILE = "log/DEBUG/"
    else:
        log_level = logging.INFO
        LOG_FILE = "log/INFO/"
    logging.basicConfig(level=log_level)  # 调试debug级(开发环境)
    file_log_handler = TimedRotatingFileHandler(
        "{}/{}.log".format(LOG_FILE, log_name),
        when="D",
        interval=7,
        backupCount=365,
        encoding="UTF-8",
        delay=False,
        utc=True
    )
    if log_name == "DEBUG":
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s')  # 时间,日志级别,记录日志文件,行数,信息
    else:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    # 将日志记录器指定日志的格式
    file_log_handler.setFormatter(formatter)
    # add filter
    # 日志等级的设置
    # 为全局的日志工具对象添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
