#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

import logging

from config import Configuration as cfg


def get_cls_logger(cls: str) -> object:
    """
    Logger config. Sets handler to a file, formater and logging level.

    :param cls:
        str Name of class where logger calling.
    :return:
        Returns Logger instans.
    """
    logger = logging.getLogger(cls)
    if not logger.handlers:
        handler = logging.FileHandler(cfg.LOG_FILE)
        formatter = logging.Formatter(
            "%(asctime)s %(name)-20s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if cfg.DEBUG else logging.INFO)
    return logger
