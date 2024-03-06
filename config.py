#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""
import os
# from os import environ as env
# from dotenv import load_dotenv
from datetime import datetime


# project_dotenv = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(project_dotenv):
    # load_dotenv(project_dotenv)

class Configuration(object):
    DEBUG = True
    SHOW_GRID = True

    # Set a list of ten main contrast colors + gray
    COLORS = [
                "#1f77b4", #  1 blue
                "#ff7f0e", #  2 orange
                "#2ca02c", #  3 green
                "#d62728", #  4 red
                "#9467bd", #  5 purple
                "#8c564b", #  6 brown
                "#e377c2", #  7 pink
                "#bc8dd8", #  8 violet 
                "#bcbd22", #  9 yellow
                "#17becf", # 10 cyan
                "#7f7f7f", # 11 gray
             ]
    CLR_NAMES = ["blue", "orange", "green", "red", "purple", "brown", "pink", "violet", "yellow", "cyan", "gray"]
    CLR_DICT = dict(zip(CLR_NAMES, COLORS))

    # Date
    CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
    IDX_STR = "{IDX}"
    TIME_UNITS = "ms"

    # Files
    USB_DEVICE = "sdb"
    USB_PART = USB_DEVICE + "1"
    USB_DRIVE = os.path.join("/dev", USB_PART)
    WRITE_TRESHOLD = 100000  # 100KB
    DATA_DIR_NAME = "data"
    REPORT_NAME = f'{CURRENT_DATE}-{IDX_STR}.pdf'
    LOG_FILE = os.path.join(os.path.dirname(__file__), "analyzer_reporter.log")

