#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project
import sys
import time
from gpiozero import LED, Button

from config import Configuration as cfg
from logger import get_cls_logger
from storage_controller import StorageController
from analyzer_controller import AnalyzerController
from signal_processor import SignalProcessor
from signal_grapher import SignalGrapher
from report_generator import ReportGenerator

# Initialize LED and Button objects
led = LED(cfg.LED_PIN)
button = Button(cfg.BUTTON_PIN)


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
    print("---------------------------------\n")

def wait_for_usb_storage_ready(usb_storage: StorageController) -> None:
    """
    Wait until USB storage is ready to write.
    """
    led.blink(on_time=cfg.BLINK_TIME, off_time=cfg.BLINK_TIME)
    print_usb_storage_info(usb_storage)
    while not usb_storage.ready_to_write:
        if usb_storage.changed and not usb_storage.ready_to_write:
            print_usb_storage_info(usb_storage)
        time.sleep(0.5)

def main() -> None:
    """
    Main function
    """
    usb_storage = StorageController()
    
    if not usb_storage.ready_to_write:
        wait_for_usb_storage_ready(usb_storage)

    led.on() # Turn LED on because relay has vice versa logic
    print_usb_storage_info(usb_storage)

    button.wait_for_press(cfg.BUTTON_TIMEOUT)
    led.blink(on_time=cfg.BLINK_TIME, off_time=cfg.BLINK_TIME)

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

        if usb_storage.changed:
            wait_for_usb_storage_ready(usb_storage)

        if usb_storage.ready_to_write:
            generator.generate_report()
            generator.save_pulse_width_csv(signal_proc.pulse_width)

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        sys.exit(0)
