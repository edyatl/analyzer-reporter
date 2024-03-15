#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project

from config import Configuration as cfg
from logger import get_cls_logger
from storage_controller import StorageController
from analyzer_controller import AnalyzerController
from signal_processor import SignalProcessor
from signal_grapher import SignalGrapher
from report_generator import ReportGenerator

def main() -> None:
    """
    Main function
    """
    usb_storage = StorageController()
    print("USB Plugged:", usb_storage.usb_plugged)
    print("Mount Point:", usb_storage.mount_point)
    print("Data Directory:", usb_storage.data_dir)
    print("PDF Files:", usb_storage.pdf_files)
    print("Last PDF Report:", usb_storage.last_pdf_report)
    print("Last PDF Report date:", usb_storage.last_pdf_report_date)
    print("Last PDF Report index:", usb_storage.last_pdf_report_idx)
    print("Current PDF Report:", usb_storage.current_pdf_report)
    print("Free Space:", usb_storage.free_space)
    print("Ready to Write:", usb_storage.ready_to_write)

    if usb_storage.ready_to_write:
        analyzer = AnalyzerController()
        df = analyzer.capture_signals()

        signal_proc = SignalProcessor(df)

        grapher = SignalGrapher(
            filtered_signals_df = signal_proc.filtered_signals_df,
            pulse_counts = signal_proc.pulse_count,
            pulse_points_width = signal_proc.pulse_points_width,
        )

        grapher.plot_signals()

        idx = (
            1
            if cfg.CURRENT_DATE != usb_storage.last_pdf_report_date
            else usb_storage.last_pdf_report_idx + 1
        )

        generator = ReportGenerator(
            figure=grapher.figure,
            report_file = usb_storage.current_pdf_report,
            attempt_number = idx,
            capture_date = cfg.CURRENT_DATE,
        )

        generator.generate_report()

if __name__ == "__main__":
    main()
