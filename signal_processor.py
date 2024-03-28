#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project

import pandas as pd
import numpy as np

from scipy import signal

from config import Configuration as cfg
from logger import get_cls_logger

class SignalProcessor:
    """Class to process signals"""

    logger = get_cls_logger(__qualname__)

    def __init__(self, signals_df: pd.DataFrame):
        self.signals_df = signals_df

        # Filter noise for each signal
        self.filtered_signals_df = self._filter_noise()

        # Find pulse pivots for each signal
        self.pulse_pivots_df = self._find_pulse_pivots()

        # Calculate pulse count and pulse width for each signal
        self.pulse_count, self.pulse_points_width = self._calculate_pulse_metrics()

        self.logger.debug("Initialized %s", self.__class__.__name__)

    def _filter_noise(self) -> pd.DataFrame:
        """Filter noise for each signal."""
        filtered_signals = {}
        for col in self.signals_df.columns:
            filtered_signals[col] = signal.medfilt(
                self.signals_df[col], cfg.FILTER_WSIZE
            )
        return pd.DataFrame(filtered_signals)

    def _find_pulse_pivots(self) -> pd.DataFrame:
        """Find pulse pivots for each signal."""
        pulse_pivots = {}
        for col in self.filtered_signals_df.columns:
            pulse_pivots[col] = np.diff(self.filtered_signals_df[col])
        return pd.DataFrame(pulse_pivots)

    def _calculate_pulse_metrics(self) -> tuple:
        """Calculate pulse count and pulse width for each signal."""
        pulse_count = {}
        pulse_points_width = {}
        for col in self.pulse_pivots_df.columns:
            pulse_count[col] = self._signal_pulse_count(self.pulse_pivots_df[col])
            pulse_points_width[col] = [
                self._signal_pulse_width(self.pulse_pivots_df[col], i)
                for i in range(pulse_count[col])
            ]
        return pulse_count, pulse_points_width

    @staticmethod
    def _signal_pulse_count(ser: pd.Series) -> int:
        """Function to calculate number of pulses."""
        return len(np.atleast_1d(ser).nonzero()[0]) // 2

    @staticmethod
    def _signal_pulse_width(ser: pd.Series, n: int) -> tuple:
        """Function to calculate pulse width."""
        n = n << 1
        ser_nonzero = np.atleast_1d(ser).nonzero()[0]
        return ser_nonzero[n], ser_nonzero[n + 1], ser_nonzero[n + 1] - ser_nonzero[n]

    @property
    def pulse_points(self) -> dict:
        """Property to access pulse points (X1, X2)."""
        return {
            k: list(map(lambda x: x[:2], v)) for k, v in self.pulse_points_width.items()
        }

    @property
    def pulse_width(self) -> dict:
        """Property to access pulse width."""
        return {
            k: list(map(lambda x: x[2], v)) for k, v in self.pulse_points_width.items()
        }

