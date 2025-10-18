# ==========================================================
#  PDF Splitter Module
#  --------------------
#  This file defines the PDFSplitter class used in main.py.
#  It uses the PyPDF2 library to split a PDF file into
#  two parts based on a page number entered by the user.
# ==========================================================

# Import PyPDF2 classes
# - PdfReader is used to read pages from an existing PDF
# - PdfWriter is used to create and save new PDF files
from PyPDF2 import PdfReader, PdfWriter

# os is used for file path manipulation (creating folders, saving files, etc.)
import os


class PDFSplitter:
    """Handles splitting of PDF files into two parts."""

    def __init__(self, file_path):
        # Store the original PDF file path when the class is initialized
        self.file_path = file_path

    def split(self, split_page: int):
        """
        Splits the PDF into two separate files.

        Args:
            split_page (int): The page number where the split occurs.
                              Example: If split_page = 5, then:
                                - part1 = pages 1–5
                                - part2 = pages 6–end

        Returns:
            tuple(str, str): Paths of the two output files created.
        """

        # --- 1️⃣ Load the input PDF file ---
        reader = PdfReader(self.file_path)
        total_pages = len(reader.pages)  # total number of pages in the file

        # --- 2️⃣ Validate split page ---
        # The page number must be within the valid range
        if split_page < 1 or split_page >= total_pages:
            raise ValueError(f"Split page must be between 1 and {total_pages - 1}")

        # --- 3️⃣ Create an output folder to save results ---
        output_dir = os.path.join(os.path.dirname(self.file_path), "split_output")
        os.makedirs(output_dir, exist_ok=True)  # create folder if not exists

        # --- 4️⃣ Create first output PDF (from page 1 to split_page) ---
        part1 = PdfWriter()
        for i in range(split_page):
            part1.add_page(reader.pages[i])  # add each page one by one

        # Build the output file name (e.g., file_part1.pdf)
        part1_path = os.path.join(
            output_dir,
            f"{os.path.splitext(os.path.basename(self.file_path))[0]}_part1.pdf"
        )

        # Save part 1
        with open(part1_path, "wb") as f:
            part1.write(f)

        # --- 5️⃣ Create second output PDF (remaining pages) ---
        part2 = PdfWriter()
        for i in range(split_page, total_pages):
            part2.add_page(reader.pages[i])

        part2_path = os.path.join(
            output_dir,
            f"{os.path.splitext(os.path.basename(self.file_path))[0]}_part2.pdf"
        )

        # Save part 2
        with open(part2_path, "wb") as f:
            part2.write(f)

        # --- 6️⃣ Return the saved file paths ---
        return part1_path, part2_path
