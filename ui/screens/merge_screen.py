# ==========================================================
# ui/screens/merge_screen.py
# ==========================================================
# Merge screen — Combine multiple PDFs in custom order
#   • Displays draggable list of PDFs
#   • Allows removing and reordering
#   • Uses PDFMerger for combining files
# ==========================================================

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from PyPDF2 import PdfReader

from ui.components.banner_message import BannerMessage
from ui.components.draggable_row import DraggableRow
from pdf_engine.pdf_merger import PDFMerger


class MergeScreen(Screen):
    """Allows user to drag, remove, and merge PDFs."""

    def on_pre_enter(self):
        """Load available sample PDFs."""
        self.ids.merge_list.clear_widgets()

        folder = "assets/samples"
        os.makedirs(folder, exist_ok=True)
        pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]

        if not pdf_files:
            BannerMessage.show(self, "No PDFs found in assets/samples", msg_type="error")
            return

        for file_name in pdf_files:
            file_path = os.path.join(folder, file_name)
            try:
                reader = PdfReader(file_path)
                num_pages = len(reader.pages)
            except Exception as e:
                num_pages = 0
                print(f"Error reading {file_name}: {e}")

            row = DraggableRow()
            row.file_path = file_path

            row.add_widget(Image(source="assets/icons/pdf_icon.png", size_hint_x=None, width=30))
            row.add_widget(Label(text=f"{file_name} ({num_pages} pages)",
                                 color=(0, 0, 0, 1), halign="left"))
            remove_btn = Button(
                background_normal="assets/icons/delete.png",
                background_down="assets/icons/delete.png",
                size_hint_x=None, width=32, background_color=(1, 0, 0, 0.1)
            )
            remove_btn.bind(on_press=lambda btn, r=row: self.remove_row(r))
            row.add_widget(remove_btn)
            self.ids.merge_list.add_widget(row)

        self.ids.merge_btn.disabled = len(pdf_files) < 2

    def remove_row(self, row):
        """Remove a selected row from the merge list."""
        self.ids.merge_list.remove_widget(row)
        BannerMessage.show(self, "Removed PDF from list.", msg_type="info")
        self.ids.merge_btn.disabled = len(self.ids.merge_list.children) < 2

    def merge_pdfs(self):
        """Merge selected PDFs in current order."""
        paths = [r.file_path for r in reversed(self.ids.merge_list.children)]
        if len(paths) < 2:
            BannerMessage.show(self, "Select at least two PDFs to merge.", msg_type="error")
            return

        try:
            merger = PDFMerger(paths)
            output_path = merger.merge()
            BannerMessage.show(self, f"Merged successfully!\nSaved at: {output_path}", msg_type="success")
        except Exception as e:
            BannerMessage.show(self, f"Merge failed: {e}", msg_type="error")
