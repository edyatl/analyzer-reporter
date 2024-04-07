#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> April 2024
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

        self.rising_signals = self._determine_rising_signals()

        self.logger.debug("Initialized %s", self.__class__.__name__)

    def _filter_noise(self) -> pd.DataFrame:
        """Filter noise for each signal."""
        return self.signals_df.apply(lambda col: signal.medfilt(col, cfg.FILTER_WSIZE))

    def _find_pulse_pivots(self) -> pd.DataFrame:
        """Find pulse pivots for each signal."""
        return self.filtered_signals_df.apply(np.diff)

    def _calculate_pulse_metrics(self) -> tuple:
        """Calculate pulse count and pulse width for each signal."""
        pulse_count = {}
        pulse_points_width = {}
        for col in self.pulse_pivots_df.columns:
            pulse_points_width[col] = self._signal_pulse_points_width(
                self.pulse_pivots_df[col]
            )
            pulse_count[col] = len(pulse_points_width[col])

        return pulse_count, pulse_points_width

    def _determine_rising_signals(self) -> dict:
        """Determine rising signals."""
        return {
            col: self._is_rising_signal(self.pulse_pivots_df[col])
            for col in self.pulse_pivots_df.columns
        }

    @staticmethod
    def _is_start_from_pulse(sig_pivots: pd.Series) -> bool:
        """Function to check if signal is start from pulse."""
        all_indices = np.atleast_1d(sig_pivots).nonzero()[0]
        differences = np.diff(all_indices)
        return np.sum(differences[::2]) < np.sum(differences[1::2])

    @staticmethod
    def _signal_pulse_points_width(sig_pivots: pd.Series) -> list:
        """Function to calculate pulses points and width."""
        all_indices = np.atleast_1d(sig_pivots).nonzero()[0]
        differences = np.diff(all_indices)
        if SignalProcessor._is_start_from_pulse(sig_pivots):
            pulses_points, pulses_width = all_indices[:], differences[::2]
        else:
            pulses_points, pulses_width = all_indices[1:], differences[1::2]

        # Ensure even number of pulse points
        if len(pulses_points) % 2 != 0:
            pulses_points = pulses_points[:-1]

        pulses_points = np.split(pulses_points, len(pulses_points) // 2)

        return [
            np.append(_point, _width)
            for _point, _width in zip(pulses_points, pulses_width)
        ]

    @staticmethod
    def _is_rising_signal(_signal: pd.Series) -> bool:
        """Function to check if signal is rising."""
        all_indices = np.atleast_1d(_signal).nonzero()[0]
        rising_edges = np.where(np.atleast_1d(_signal) == 1)[0]
        first_edge_is_rising = all_indices[0] == rising_edges[0]

        if SignalProcessor._is_start_from_pulse(_signal):
            return first_edge_is_rising
        return not first_edge_is_rising

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

