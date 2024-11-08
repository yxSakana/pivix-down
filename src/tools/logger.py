# -*- coding: UTF-8 -*-
# @Filename: logger.py
# @Author: sxy
# @Date: 2023-05-29 16:21

import os
import logging.config

reset_color = "\033[0m"
thread_id_color = "\033[4m"
time_color = "\033[90m"
module_color = "\033[94m"
color = {
    "DEBUG": "",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[101m"
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        result = (
                # f"({module_color}{record.filename}{reset_color}:{record.lineno})" +
                f"({module_color}{record.name}{reset_color}:{record.lineno})" +
                f"{color[record.levelname]}[{record.levelname}]{reset_color}" +
                f"{time_color}[{self.formatTime(record, self.datefmt)}]{reset_color} " +
                f"{color[record.levelname]}{record.getMessage()}{reset_color}"
        )
        return result


class LoggerConfig(object):
    def __init__(self, name: str, filename: str = None):
        self.name = name
        self.filename = filename if filename is not None else f"log/{name}"

        # level config configure
        self.level_config = {
            "logger": {
                "root": "INFO",
                self.name: "INFO"
            },
            "console": {
                "root": "DEBUG",
                self.name: "DEBUG"
            }
        }
        # logger configure
        self.log_config = {
            "version": 1,
            # Formatter settings 格式化设置
            "formatters": {
                "loggerFormatter": {
                    # "format": "(%(module)s:%(lineno)s)[%(levelname)s][%(asctime)s]: %(message)s",
                    "format": "(%(name)s:{lineno})[%(levelname)s][%(asctime)s]: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
                "colorFormatter": {
                    "()": CustomFormatter,
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
            },
            "filters": {},
            # Handler settings
            "handlers": {
                # console Handler -- settings of "root"
                "consoleHandler": {
                    "class": "logging.StreamHandler",
                    "level": self.level_config["console"]["root"],
                    "formatter": "colorFormatter",
                    "stream": "ext://sys.stdout"
                },
                # color Handler -- settings of "self.name logger"
                "coloredHandler": {
                    "class": "logging.StreamHandler",
                    "level": self.level_config["console"][self.name],
                    "formatter": "colorFormatter",
                    "stream": "ext://sys.stdout"
                }
            },
            # logger settings
            # root
            "root": {
                "level": self.level_config["logger"]["root"],
                "handlers": ["consoleHandler"]
            },
            # create logger config
            "loggers": {
                self.name: {
                    "level": self.level_config["logger"][self.name],
                    "propagate": 0,
                    "handlers": ["coloredHandler"]
                }
            },
            "incremental": False,
            "disable_existing_loggers": False
        }

        if self.filename:
            self.log_config["handlers"]["fileHandler"] = {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "loggerFormatter",
                    "filename": self.filename,
                    "mode": "a",  # mode
                    "maxBytes": 102400,  # 最大文件大小
                    "backupCount": 10,  # 保留的文件个数
                    "encoding": "utf-8",
                    "delay": False  # 延迟
            }
            self.log_config["loggers"][self.name]["handlers"] = ["fileHandler"]


def get_module_name() -> str:
    """get current module name

    :return str: module
    """
    current_dir = os.getcwd()
    project_name = os.path.basename(current_dir)

    return project_name


def get_logger(name: str, filename: str="") -> logging.Logger:
    """create by name

    :param str name: name
    :return logging.Logger: logger
    """
    log_config = LoggerConfig(name, filename)
    logging.config.dictConfig(log_config.log_config)
    logger = logging.getLogger(name)

    return logger


def get_module_logger() -> logging.Logger:
    """get logger by current mdule name create

    :return logging.Logger: logger
    """
    module_name = get_module_name()

    return get_logger(module_name)


def set_level(logger, level: str):
    if level.lower() == "debug":
        logger.handlers[0].setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    elif level.lower() == "info":
        logger.handlers[0].setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
    elif level.lower() == "warring":
        logger.handlers[0].setLevel(logging.WARNING)
        logger.setLevel(logging.WARNING)
    elif level.lower() == "error":
        logger.handlers[0].setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
    elif level.lower() == "critical":
        logger.handlers[0].setLevel(logging.CRITICAL)
        logger.setLevel(logging.CRITICAL)
