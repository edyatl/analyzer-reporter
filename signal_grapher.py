#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import figure as pltfg

from config import Configuration as cfg
from logger import get_cls_logger


class SignalGrapher:
    """Class to plot signals on a matplotlib figure."""

    logger = get_cls_logger(__qualname__)

    def __init__(
        self,
        filtered_signals_df: pd.DataFrame,
        pulse_counts: dict,
        pulse_points_width: dict,
        rising_signals: dict,
    ) -> None:
        """
        Initialize SignalGrapher.

        :param filtered_signals_df: DataFrame of filtered signals.
        :param pulse_counts: Dictionary of pulse counts for each signal.
        :param pulse_points_width: Dictionary of pulse points and widths for each signal.
        """
        self.filtered_signals_df = filtered_signals_df
        self.pulse_counts = pulse_counts
        self.pulse_points_width = pulse_points_width
        self.rising_signals = rising_signals
        self.signals_to_plot_widths: list = self._get_signals_to_plot()
        self.vlines: list = []
        self.figure: pltfg.Figure = None

        self.logger.debug("Initialized %s", self.__class__.__name__)

    def plot_signals(self) -> None:
        """Plot signals and pulses."""
        # Set A4 canvas size in inches
        a4_width_inches = 8.27
        a4_height_inches = 11.69
        bot_mrg = (
            1 - self.filtered_signals_df.shape[1] / 10
            if self.filtered_signals_df.shape[1] < 10
            else 0.1
        )

        fig, axes = plt.subplots(
            self.filtered_signals_df.shape[1],
            1,
            sharex="col",
            figsize=(a4_width_inches, a4_height_inches * 0.85),
        )

        for i, col in enumerate(self.filtered_signals_df.columns):
            axes[i].step(
                self.filtered_signals_df.index,
                self.filtered_signals_df[col],
                cfg.COLORS[i],
            )
            axes[i].set_ylabel(col)

            if col in self.signals_to_plot_widths:
                for x1, x2, width in self.pulse_points_width[col]:
                    self._plot_pulse_width(axes[i], x1, x2, width)

        for ax in axes:
            ax.grid(cfg.SHOW_GRID)

            for vline in self.vlines:
                self._plot_vertical_lines(ax, vline)

        fig.subplots_adjust(
            left=0.12, right=0.95, bottom=bot_mrg, top=0.95, wspace=0.4, hspace=0.4
        )
        plt.xlabel("Time (ms)")

        self.figure = fig

    def _plot_pulse_width(self, ax: plt.Axes, x1: int, x2: int, width: int) -> None:
        """Plot pulse width."""
        ax.annotate(
            "",
            xy=(x1, 0.5),
            xytext=(x2, 0.5),
            arrowprops={"arrowstyle": "<->", "color": cfg.CLR_DICT["gray"]},
        )
        ax.text(
            (x1 + x2) / 2, 0.6, f"{width} ms", ha="center", color=cfg.CLR_DICT["gray"]
        )

    def _plot_vertical_lines(self, ax: plt.Axes, vline_x: int) -> None:
        """Plot vertical dashed lines."""
        ax.axvline(vline_x, color=cfg.CLR_DICT["purple"], linestyle="--")

    def _get_signals_to_plot(self) -> list:
        """Get the list of signal names to plot based on cfg.PLOT_WIDTH value."""
        if cfg.PLOT_WIDTH == "all":
            return list(self.rising_signals.keys())
        elif cfg.PLOT_WIDTH == "rising":
            return [key for key, value in self.rising_signals.items() if value]
        elif cfg.PLOT_WIDTH == "falling":
            return [key for key, value in self.rising_signals.items() if not value]
        return []

    def add_vlines(self, vlines: list) -> None:
        """Add vertical dashed lines."""
        self.vlines = vlines

