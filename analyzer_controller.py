#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project

import os
import io
import subprocess
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

    def capture_signals(self) -> pd.DataFrame:
        """
        Capture signals from Hantek 4032L logic analyzer.
        If real capturing is not available yet, loads sample data from file.
        """
        if self.real_capture:
            # Retry capturing for a few attempts if an error occurs
            for attempt in range(1, cfg.MAX_CAPTURE_ATTEMPTS + 1):
                try:
                    # Perform real capturing using sigrok-cli and store the output in a buffer
                    command = cfg.CAPTURE_COMMAND
                    process = subprocess.Popen(command, stdout=subprocess.PIPE)
                    output, _ = process.communicate()
                    output_str = output.decode("utf-8")

                    # Convert the output to a pandas DataFrame
                    df = pd.read_csv(io.StringIO(output_str))
                    self.logger.debug("Buffer after sigrok-cli loaded to DataFrame: %s rows", df.shape[0])
                    return df

                except subprocess.CalledProcessError as e:
                    self.logger.error("Error occurred while capturing signals: %s", str(e))
                    self.logger.debug("Attempting to capture signals again (Attempt %d/%d)",
                                     attempt, cfg.MAX_CAPTURE_ATTEMPTS)
                    time.sleep(cfg.RETRY_DELAY_SECONDS)

                except pd.errors.ParserError as e:
                    self.logger.error("Error occurred while parsing output: %s", str(e))
                    self.logger.debug("Attempting to capture signals again (Attempt %d/%d)",
                                     attempt, cfg.MAX_CAPTURE_ATTEMPTS)
                    time.sleep(cfg.RETRY_DELAY_SECONDS)

            self.logger.error("Failed to capture signals after %d attempts", cfg.MAX_CAPTURE_ATTEMPTS)
            return pd.DataFrame()
        else:
            # Try to load sample data from file and if error on parse or file not found, return empty DataFrame
            try:
                df = pd.read_csv(self.data_path)
                self.logger.debug("Data loaded from file: %s", self.data_path)
                return df
            except (pd.errors.ParserError, FileNotFoundError) as e:
                self.logger.error("Error occurred while loading sample data: %s", str(e))
                return pd.DataFrame()

