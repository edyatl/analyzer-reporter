#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project

import os

from config import Configuration as cfg
from logger import get_cls_logger


class StorageController:
    """Class to control USB storage"""

    logger = get_cls_logger(__qualname__)

    def __init__(self):
        self.logger.debug("Initialized %s", self.__class__.__name__)
        self.usb_plugged = self.check_usb_plugged()
        self.usb_mounted = False
        self.mount_point = None
        self.data_dir = None
        self.pdf_files = []
        self.last_pdf_report = None
        self.last_pdf_report_date = None
        self.last_pdf_report_idx = 0
        self.current_pdf_report = None
        self.current_pdf_report_idx = 0
        self.free_space = 0
        self.ready_to_write = False
        self.update()

    def update(self) -> None:
        """Update instance variables."""
        self.reset()

        if self.usb_plugged:
            self.get_mount_point()

            if self.usb_mounted:
                self._create_data_directory()
                self.get_pdf_files()
                self.get_last_pdf_report()
                self.get_last_pdf_report_date()
                self.get_last_pdf_report_idx()
                self._set_current_pdf_report()
                self.get_free_space()

                if self.free_space > cfg.WRITE_TRESHOLD:
                    self.ready_to_write = True

    def reset(self) -> None:
        """Reset instance variables."""
        self.usb_plugged = self.check_usb_plugged()
        self.usb_mounted = False
        self.mount_point = None
        self.data_dir = None
        self.pdf_files = []
        self.last_pdf_report = None
        self.last_pdf_report_date = None
        self.last_pdf_report_idx = 0
        self.current_pdf_report = None
        self.current_pdf_report_idx = 0
        self.free_space = 0
        self.ready_to_write = False

    def get_mount_point(self) -> None:
        """Get the mount point of the USB drive."""
        with open("/proc/mounts", "r", encoding="utf-8") as mounts:
            for line in mounts:
                if cfg.USB_DRIVE in line:
                    self.usb_mounted = True
                    self.mount_point = line.split()[1]
                    break

    def _create_data_directory(self) -> None:
        """Get or create data directory if it doesn't exist."""
        self.data_dir = os.path.join(self.mount_point, cfg.DATA_DIR_NAME)
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def get_pdf_files(self) -> None:
        """Get a list of PDF files in the data directory."""
        self.pdf_files = [
            f for f in os.listdir(self.data_dir) if f.lower().endswith(".pdf")
        ]

    def get_last_pdf_report(self) -> None:
        """Get the last PDF report file."""
        if self.pdf_files:
            self.last_pdf_report = sorted(self.pdf_files)[-1]

    def get_last_pdf_report_date(self) -> None:
        """Extract the date from the last PDF report file."""
        if self.last_pdf_report:
            self.last_pdf_report_date = "-".join(self.last_pdf_report.split("-")[:3])

    def get_last_pdf_report_idx(self) -> None:
        """Extract the index from the last PDF report file."""
        if self.last_pdf_report:
            self.last_pdf_report_idx = int(
                self.last_pdf_report.split("-")[3].split(".")[0]
            )

    def _set_current_pdf_report(self) -> None:
        """Set the current PDF report file index and full path."""
        self.current_pdf_report_idx = (
            1
            if cfg.CURRENT_DATE != self.last_pdf_report_date
            else self.last_pdf_report_idx + 1
        )
        self.current_pdf_report = os.path.join(
            self.data_dir,
            cfg.REPORT_NAME.format(IDX=str(self.current_pdf_report_idx).zfill(3)),
        )

    def get_free_space(self) -> None:
        """Get the free space in the USB drive."""
        statvfs: os.statvfs = os.statvfs(self.mount_point)
        self.free_space = statvfs.f_frsize * statvfs.f_bavail

    @staticmethod
    def check_usb_plugged() -> bool:
        """Check if USB is plugged in."""
        return os.path.exists(cfg.USB_DRIVE)

    @property
    def changed(self) -> bool:
        """Check for USB storage status."""
        previous_usb_plugged = self.usb_plugged
        previous_usb_mounted = self.usb_mounted
        previous_ready_to_write = self.ready_to_write

        self.update()

        return (
            previous_usb_plugged != self.usb_plugged
            or previous_usb_mounted != self.usb_mounted
            or previous_ready_to_write != self.ready_to_write
        )
