#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""
import os
from datetime import datetime


class Configuration(object):
    # Debugging
    DEBUG = True

    # Plotting
    SHOW_GRID = True              # Show grid in plots
    TIME_UNITS = "ms"

    # Define GPIO pin numbers
    LED_PIN = 23
    BUTTON_PIN = 24

    # Interface
    BLINK_TIME = 0.25
    BUTTON_TIMEOUT = None         # 15

    # Signal Processing
    FILTER_WSIZE = 15

    # Data Capture
    REAL_CAPTURE = False          # Real capturing is not available yet
    EXAMPLE_DATA = "data4.csv"    # Sample data instead of real capturing
    EXAMPLE_DATA_DIR = "../"
    CAPTURE_COMMAND = [
        "sigrok-cli",
        "--driver",
        "hantek-4032l",
        "--channels",
        "A0=AS4_2,A1=AS4_4,A2=AS3_2,A3=AS3_4,A4=AS6_2,A5=AS6_4,A6=AS7_2,A7=AS7_4,A8=AS1_4,A9=AS2_4",
        "--output-format",
        "csv:label=channel:header=false",
        "--config",
        "samplerate=1000",
        "--samples",
        "4096",
    ]
    MAX_CAPTURE_ATTEMPTS = 3
    RETRY_DELAY_SECONDS = 2

    # Reporting
    ATTEMPT_POINT = (470, 767)    # XY point of attempt number in report canvas
    DATE_POINT = (470, 752)       # XY point of date in report canvas
    CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

    # USB Storage
    USB_DEVICE = "sdb"            # Change it to sda on Raspberry Pi
    USB_PART = USB_DEVICE + "1"
    USB_DRIVE = os.path.join("/dev", USB_PART)
    WRITE_TRESHOLD = 100000       # 100KB

    # Paths and Files
    DATA_DIR_NAME = "data"
    IDX_STR = "{IDX}"
    REPORT_NAME = f'{CURRENT_DATE}-{IDX_STR}.pdf'
    TEMPLATE_FILE = os.path.join(os.path.abspath("../"), "template2.pdf")
    LOG_FILE = os.path.join(os.path.dirname(__file__), "analyzer_reporter.log")

    # Colors Definition
    COLORS = [
        "#1f77b4",  #  1 blue
        "#ff7f0e",  #  2 orange
        "#2ca02c",  #  3 green
        "#d62728",  #  4 red
        "#9467bd",  #  5 purple
        "#8c564b",  #  6 brown
        "#e377c2",  #  7 pink
        "#bc8dd8",  #  8 violet
        "#bcbd22",  #  9 yellow
        "#17becf",  # 10 cyan
        "#7f7f7f",  # 11 gray
    ]
    CLR_NAMES = [
        "blue",
        "orange",
        "green",
        "red",
        "purple",
        "brown",
        "pink",
        "violet",
        "yellow",
        "cyan",
        "gray",
    ]
    CLR_DICT = dict(zip(CLR_NAMES, COLORS))

