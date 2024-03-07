#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project

import os
import pandas as pd

from config import Configuration as cfg
from logger import get_cls_logger

class AnalyzerController:
    """Class to control Hantek 4032L logic analyzer"""

    logger = get_cls_logger(__qualname__)

    def __init__(self):
        self.real_capture = cfg.REAL_CAPTURE
        self.data_path = os.path.join(
            os.path.abspath(cfg.EXAMPLE_DATA_DIR), cfg.EXAMPLE_DATA
        )

        self.logger.debug("Make an instance of %s class", self.__class__.__name__)

    def capture_signals(self):
        """
        Capture signals from Hantek 4032L logic analyzer.
        If real capturing is not available yet, loads sample data from file.
        """
        if self.real_capture:
            # Perform real capturing using sigrok-cli
            # Capture signals with sigrok-cli command
            # Replace the following line with the actual sigrok-cli command for capturing signals
            self.logger.debug(
                "Start block with sigrok-cli. Real captur: %s", self.real_capture
            )
            # Returns empty DataFrame
            return pd.DataFrame()
        else:
            # Load sample data from exaplle data file
            df = pd.read_csv(self.data_path)
            self.logger.debug("Data loaded from file: %s", self.data_path)
            return df

