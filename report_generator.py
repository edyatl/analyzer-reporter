#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
    Developed by @edyatl <edyatl@yandex.ru> March 2024
    https://github.com/edyatl

"""

# This file is part of the analyzer_reporter project

import io

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import figure as pltfg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from pypdf import PdfReader, PdfWriter

from config import Configuration as cfg
from logger import get_cls_logger

class ReportGenerator:
    """Class to generate PDF report."""

    logger = get_cls_logger(__qualname__)

    def __init__(
        self,
        figure: pltfg.Figure,
        report_file: str,
        attempt_number: int,
        capture_date: str,
    ):
        """Initialize ReportGenerator."""
        self.figure = figure
        self.report_file = report_file
        self.attempt_number = str(attempt_number).zfill(3)
        self.capture_date = capture_date
        self.template = self._load_template()

        self.add_text(self.attempt_number, cfg.ATTEMPT_POINT)
        self.add_text(self.capture_date, cfg.DATE_POINT)

        self.logger.debug("Initialized %s", self.__class__.__name__)

    def _load_template(self) -> io.BytesIO:
        """Load PDF template."""
        template = io.BytesIO()
        with open(cfg.TEMPLATE_FILE, "rb") as f:
            template.write(f.read())
        template.seek(0)
        return template

    def add_text(self, text: str, point: tuple) -> None:
        """Add text to the template."""
        text_pdf = self._create_text_pdf(text, point)
        text_page = PdfReader(text_pdf).pages[0]

        pdf_reader = PdfReader(self.template)
        template_page = pdf_reader.pages[0]

        template_page.merge_page(page2=text_page)

        writer = PdfWriter()
        writer.append_pages_from_reader(pdf_reader)
        writer.write(self.template)

    def _create_text_pdf(self, text: str, point: tuple) -> io.BytesIO:
        """Create PDF with text."""
        text_pdf = io.BytesIO()
        c = canvas.Canvas(text_pdf, pagesize=A4)
        c.drawString(point[0], point[1], text)
        c.save()
        text_pdf.seek(0)
        return text_pdf

    def generate_report(self) -> None:
        """Generate PDF report."""
        figure_pdf = self._save_figure_to_pdf()
        figure_page = PdfReader(figure_pdf).pages[0]

        pdf_reader = PdfReader(self.template)
        template_page = pdf_reader.pages[0]

        template_page.merge_page(page2=figure_page)

        writer = PdfWriter()
        writer.append_pages_from_reader(pdf_reader)

        with open(self.report_file, "wb") as fp:
            writer.write(fp)

    def _save_figure_to_pdf(self) -> io.BytesIO:
        """Save figure to PDF."""
        figure_pdf = io.BytesIO()
        with PdfPages(figure_pdf) as pdf:
            pdf.savefig(self.figure)
        figure_pdf.seek(0)
        return figure_pdf

