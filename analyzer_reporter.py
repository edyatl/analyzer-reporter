#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project
import sys
from gpiozero import LED, Button

from config import Configuration as cfg
from logger import get_cls_logger
from storage_controller import StorageController
from analyzer_controller import AnalyzerController
from signal_processor import SignalProcessor
from signal_grapher import SignalGrapher
from report_generator import ReportGenerator

# Define GPIO pin numbers
LED_PIN = 23
BUTTON_PIN = 24

# Initialize LED and Button objects
led = LED(LED_PIN)
button = Button(BUTTON_PIN)

def print_usb_storage_info(usb_storage: StorageController) -> None:
    """
    Print information about USB storage.
    """
    print("USB Plugged:", usb_storage.usb_plugged)
    print("USB Mounted:", usb_storage.usb_mounted)
    print("Mount Point:", usb_storage.mount_point)
    print("Data Directory:", usb_storage.data_dir)
    print("PDF Files:", usb_storage.pdf_files)
    print("Last PDF Report:", usb_storage.last_pdf_report)
    print("Last PDF Report date:", usb_storage.last_pdf_report_date)
    print("Last PDF Report index:", usb_storage.last_pdf_report_idx)
    print("Current PDF Report:", usb_storage.current_pdf_report)
    print("Free Space:", usb_storage.free_space)
    print("Ready to Write:", usb_storage.ready_to_write)

def main() -> None:
    """
    Main function
    """
    led.blink(on_time=0.25, off_time=0.25)

    usb_storage = StorageController()
    print_usb_storage_info(usb_storage)

    while not usb_storage.ready_to_write:
        led.blink(on_time=0.25, off_time=0.25)
        usb_storage = StorageController()

    print_usb_storage_info(usb_storage)

    if usb_storage.ready_to_write:
        led.off() # Turn LED on because relay has vice versa logic

        button.wait_for_press()

        led.blink(on_time=0.25, off_time=0.25)

        analyzer = AnalyzerController()
        df = analyzer.capture_signals()
        
        if not df.empty:
            signal_proc = SignalProcessor(df)

            grapher = SignalGrapher(
                filtered_signals_df = signal_proc.filtered_signals_df,
                pulse_counts = signal_proc.pulse_count,
                pulse_points_width = signal_proc.pulse_points_width,
            )

            grapher.plot_signals()

            generator = ReportGenerator(
                figure=grapher.figure,
                report_file = usb_storage.current_pdf_report,
                attempt_number = usb_storage.current_pdf_report_idx,
                capture_date = cfg.CURRENT_DATE,
            )

            generator.generate_report()
            generator.save_pulse_width_csv(signal_proc.pulse_width)

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        sys.exit(0)
