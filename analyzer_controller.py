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

    def capture_signals(self):
        """
        Capture signals from Hantek 4032L logic analyzer.
        If real capturing is not available yet, loads sample data from file.
        """
        if self.real_capture:
            # Perform real capturing using sigrok-cli and store the output in a buffer
            command = [
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
                "2048",
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            output, _ = process.communicate()
            output_str = output.decode("utf-8")

            # Convert the output to a pandas DataFrame
            df = pd.read_csv(io.StringIO(output_str))
            return df
        else:
            # Load sample data from example data file
            df = pd.read_csv(self.data_path)
            self.logger.debug("Data loaded from file: %s", self.data_path)
            return df

