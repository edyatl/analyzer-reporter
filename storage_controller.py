#!/usr/bin/env python3
#-*- coding: utf-8 -*-
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
        self.usb_plugged: bool = self.check_usb_plugged()
        self.mount_point: str = None
        self.data_dir: str = None
        self.pdf_files: list = []
        self.last_pdf_report: str = None
        self.last_pdf_report_date: str = None
        self.last_pdf_report_idx: int = 0
        self.current_pdf_report: str = None
        self.free_space: int = 0
        self.ready_to_write: bool = False

        if self.usb_plugged:
            self.get_mount_point()
            self.create_data_directory()
            self.get_pdf_files()
            self.get_last_pdf_report()
            self.get_last_pdf_report_date()
            self.get_last_pdf_report_idx()
            self.set_current_pdf_report()
            self.get_free_space()

            if self.free_space > cfg.WRITE_TRESHOLD:
                self.ready_to_write = True

        self.logger.debug("Make an instance of %s class", self.__class__.__name__)
        self.logger.debug("USB Plugged: %s", self.usb_plugged)
        self.logger.debug("Mount Point: %s", self.mount_point)
        self.logger.debug("Data Directory: %s", self.data_dir)
        self.logger.debug("Last PDF Report: %s", self.last_pdf_report)
        self.logger.debug("Last PDF Report date: %s", self.last_pdf_report_date)
        self.logger.debug("Last PDF Report index: %s", self.last_pdf_report_idx)
        self.logger.debug("Current PDF Report: %s", self.current_pdf_report)
        self.logger.debug("Free Space: %s", self.free_space)
        self.logger.debug("Ready to Write: %s", self.ready_to_write)

    def check_usb_plugged(self) -> bool:
        return os.path.exists(cfg.USB_DRIVE)

    def get_mount_point(self) -> None:
        with open("/proc/mounts") as mounts:
            for line in mounts:
                if cfg.USB_DRIVE in line:
                    self.mount_point = line.split()[1]
                    break

    def create_data_directory(self) -> None:
        self.data_dir = os.path.join(self.mount_point, cfg.DATA_DIR_NAME)
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def get_pdf_files(self) -> None:
        self.pdf_files = [
            f for f in os.listdir(self.data_dir) if f.lower().endswith(".pdf")
        ]

    def get_last_pdf_report(self) -> None:
        if self.pdf_files:
            self.last_pdf_report = sorted(self.pdf_files)[-1]

    def get_last_pdf_report_date(self) -> None:
        if self.last_pdf_report:
            self.last_pdf_report_date = "-".join(self.last_pdf_report.split("-")[:3])

    def get_last_pdf_report_idx(self) -> None:
        if self.last_pdf_report:
            self.last_pdf_report_idx = int(
                self.last_pdf_report.split("-")[3].split(".")[0]
            )

    def set_current_pdf_report(self) -> None:
        idx = (
            1
            if cfg.CURRENT_DATE != self.last_pdf_report_date
            else self.last_pdf_report_idx + 1
        )
        self.current_pdf_report = os.path.join(
            self.data_dir, cfg.REPORT_NAME.format(IDX=str(idx).zfill(3))
        )

    def get_free_space(self) -> None:
        statvfs: os.statvfs = os.statvfs(self.mount_point)
        self.free_space = statvfs.f_frsize * statvfs.f_bavail

