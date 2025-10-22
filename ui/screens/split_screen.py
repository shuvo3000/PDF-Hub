# ==========================================================
# ui/screens/split_screen.py
# ==========================================================
# Split screen — Allows user to split PDFs by page number
#   • Lists available PDFs
#   • Lets users enter a split page number
#   • Uses BannerMessage for feedback
# ==========================================================

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from PyPDF2 import PdfReader

from ui.components.banner_message import BannerMessage
from pdf_engine.pdf_splitter import PDFSplitter


class SplitScreen(Screen):
    """Displays PDFs and allows splitting by page number."""

    def on_pre_enter(self):
        """Rebuild grid of sample PDFs when entering Split tab."""
        self.ids.split_grid.clear_widgets()

        folder = "assets/samples"
        os.makedirs(folder, exist_ok=True)
        pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]

        if not pdf_files:
            self.ids.split_grid.add_widget(Label(text="No PDF files found.", color=(0.2, 0.2, 0.2, 1)))
            return

        for pdf_file in pdf_files:
            path = os.path.join(folder, pdf_file)
            try:
                reader = PdfReader(path)
                num_pages = len(reader.pages)
            except Exception as e:
                num_pages = 0
                print(f"⚠️ Error reading {pdf_file}: {e}")

            row = GridLayout(cols=4, size_hint_y=None, height=dp(60), spacing=dp(10))

            checkbox = CheckBox(size_hint_x=None, width=dp(30))
            icon = Image(source="assets/icons/pdf_icon.png", size_hint_x=None, width=dp(28))
            label = Label(text=f"{pdf_file} ({num_pages} pages)", color=(0, 0, 0, 1), halign="left")
            textbox = TextInput(
                hint_text=f"1–{num_pages}" if num_pages else "Page #",
                input_filter="int",
                size_hint_x=None,
                width=dp(80)
            )
            textbox.max_page = num_pages

            row.add_widget(checkbox)
            row.add_widget(icon)
            row.add_widget(label)
            row.add_widget(textbox)
            self.ids.split_grid.add_widget(row)

    def process_split(self):
        """Split selected PDFs based on page input."""
        selected = 0

        for row in self.ids.split_grid.children:
            widgets = row.children[::-1]  # Keep order: checkbox, icon, label, textbox
            checkbox, icon, label, textbox = widgets
            if checkbox.active:
                selected += 1
                filename = label.text.split(" (")[0]
                pdf_path = os.path.join("assets/samples", filename)
                try:
                    if not textbox.text.strip():
                        raise ValueError("Please enter a page number.")
                    page = int(textbox.text.strip())
                    max_page = getattr(textbox, "max_page", 0)
                    if page <= 0 or page >= max_page:
                        raise ValueError(f"Page must be between 1 and {max_page - 1}.")
                    splitter = PDFSplitter(pdf_path)
                    splitter.split(page)
                    BannerMessage.show(self, f"✅ {filename} split successfully!", msg_type="success")
                except Exception as e:
                    BannerMessage.show(self, str(e), msg_type="error")

        if selected == 0:
            BannerMessage.show(self, "Please select at least one PDF.", msg_type="error")
