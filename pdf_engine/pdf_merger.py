# ==========================================================
#  PDF Merger Module
#  -----------------
#  This file defines the PDFMerger class used in main.py.
#  It merges multiple PDF files into a single PDF using PyPDF2.
# ==========================================================

from PyPDF2 import PdfReader, PdfWriter
import os
import time


class PDFMerger:
    """Handles merging of multiple PDF files."""

    def __init__(self, file_paths: list[str]):
        """
        Initialize with a list of PDF file paths.

        Args:
            file_paths (list[str]): Full paths to PDFs to merge, in order.
        """
        self.file_paths = file_paths

    def merge(self) -> str:
        """
        Merge all PDFs into one output file.

        Returns:
            str: Full path of the merged output PDF.
        """
        if not self.file_paths or len(self.file_paths) < 2:
            raise ValueError("At least two PDF files are required to merge.")

        # --- 1️⃣ Create output directory ---
        output_dir = os.path.join("assets", "output")
        os.makedirs(output_dir, exist_ok=True)

        # --- 2️⃣ Create a writer instance ---
        writer = PdfWriter()

        # --- 3️⃣ Loop through files and append pages ---
        for path in self.file_paths:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)

        # --- 4️⃣ Build unique filename ---
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"merged_{timestamp}.pdf"
        output_path = os.path.join(output_dir, filename)

        # --- 5️⃣ Write merged file ---
        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path
