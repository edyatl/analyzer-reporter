#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# Standard imports os pandas numpy matplotlib.pyplot seaborn scipy
import os

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from scipy import signal


# Temporary decision to load data
csv_data = os.path.join(os.path.abspath("../"), "data4.csv")
df = pd.read_csv(csv_data)

def noise_filter(ser: pd.Series) -> np.array:
    """
    Function to filter noise in signal

    :param ser: pd.Series
    :return: np.array
    """
    return signal.medfilt(ser, 15)

def signal_pulse_pivots(ser: pd.Series) -> np.array:
    """
    Function to find pulse pivots to measure the signal pulse width

    :param ser: pd.Series
    :return: np.array
    """
    return np.diff(ser)

# Function to calculate number of pulses
def signal_pulse_count(ser: pd.Series) -> int:
    """
    Function to calculate number of pulses

    :param ser: pd.Series
    :return: int
    """
    return len(np.where(ser != 0)[0]) // 2

def signal_pulse_width(ser: pd.Series, n: int) -> tuple:
    """
    Function measures the signal n pulse width and returns tuple 
    (nth pulse x1 point, nth pulse x2 point, pulse time interval)

    :param ser: pd.Series
    :param n: int
    :return: tuple
    """
    n = n + 1 if n > 0 else 0
    return (
        np.where(ser != 0)[0][n],
        np.where(ser != 0)[0][n + 1],
        np.where(ser != 0)[0][n + 1] - np.where(ser != 0)[0][n],
    )

def plot_width(x1: int, x2: int, width: int, i: int) -> None:
    """
    Function to plot pulse width

    :param x1: int
    :param x2: int
    :param width: int
    :param i: int
    :return: None
    """
    axes[i].axvline(x1, color="gray")
    axes[i].axvline(x2, color="gray")
    axes[i].annotate(
        "",
        xy=(x1, 0.5),
        xytext=(x2, 0.5),
        arrowprops=dict(arrowstyle="<->", color="gray"),
    )
    axes[i].text(
        (x1 + x2) / 2,
        0.6,
        f"{width} ms",
        ha="center",
        color="gray",
    )

class LogicAnalyzerController:
    pass

class SignalDataProcessor:
    pass

class StorageChecker:
    pass

class ReportGenerator:
    pass

def main() -> None:
    """
    Main function
    """
    pass

if __name__ == "__main__":
    main()
