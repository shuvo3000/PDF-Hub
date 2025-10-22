# ==========================================================
# ui/screens/home_screen.py
# ==========================================================
# Home screen — Displays quick access, recent PDFs, and actions
#   • Shows the app logo or branding area
#   • Displays list of recent files (from recent.json)
#   • Buttons: Open PDF, Open Folder
# ==========================================================

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

from ui.components.banner_message import BannerMessage
import os
import json


class HomeScreen(Screen):
    """
    Home screen showing:
      - App logo / title
      - Recently opened PDFs
      - Buttons for quick actions (Open PDF, Open Folder)
    """

    def on_pre_enter(self):
        """Refresh recent files list when entering the Home tab."""
        self.build_ui()

    def build_ui(self):
        """Create the home screen layout dynamically."""
        self.clear_widgets()
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(15))

        # --- App Logo / Branding ---
        logo = Image(source="assets/icons/app_logo.png", size_hint_y=None, height=dp(100))
        layout.add_widget(logo)
        layout.add_widget(Label(text="[b]Welcome to PDFhub[/b]", markup=True,
                                font_size=22, color=(0.1, 0.1, 0.1, 1),
                                size_hint_y=None, height=dp(30)))

        # --- Recent Files Section ---
        layout.add_widget(Label(text="Recent Files:", font_size=18,
                                color=(0.2, 0.2, 0.2, 1),
                                size_hint_y=None, height=dp(25)))

        grid = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        recent_path = os.path.join(os.path.expanduser("~"), "Documents", "PDFHub", "recent.json")
        if os.path.exists(recent_path):
            with open(recent_path, "r") as f:
                recent_files = json.load(f)
        else:
            recent_files = []

        if not recent_files:
            grid.add_widget(Label(text="No recent files found.",
                                  color=(0.4, 0.4, 0.4, 1),
                                  size_hint_y=None, height=dp(40)))
        else:
            for pdf_path in reversed(recent_files[-5:]):
                filename = os.path.basename(pdf_path)
                row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(40), spacing=dp(10))

                label = Label(text=filename, color=(0, 0, 0, 1), halign="left", valign="middle")
                label.bind(size=label.setter("text_size"))

                open_btn = Button(text="Edit", size_hint_x=None, width=dp(70))
                split_btn = Button(text="Add to Split", size_hint_x=None, width=dp(100))
                merge_btn = Button(text="Add to Merge", size_hint_x=None, width=dp(110))

                open_btn.bind(on_release=lambda x, path=pdf_path: self.open_in_editor(path))
                split_btn.bind(on_release=lambda x, path=pdf_path: self.add_to_split(path))
                merge_btn.bind(on_release=lambda x, path=pdf_path: self.add_to_merge(path))

                row.add_widget(label)
                row.add_widget(open_btn)
                row.add_widget(split_btn)
                row.add_widget(merge_btn)
                grid.add_widget(row)

        layout.add_widget(grid)

        # --- Bottom Buttons ---
        button_row = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(60))
        open_btn = Button(text="📂 Open PDF", on_release=lambda x: self.open_pdf())
        folder_btn = Button(text="🗂 Open PDFHub Folder", on_release=lambda x: self.open_folder())
        button_row.add_widget(open_btn)
        button_row.add_widget(folder_btn)
        layout.add_widget(button_row)

        self.add_widget(layout)

    # ------------------------------------------------------
    # Helper actions
    # ------------------------------------------------------
    def open_pdf(self):
        """Trigger app-level file picker via controller."""
        app = self.manager.app
        app.controller.on_open_pdf_file()

    def open_folder(self):
        """Open the user’s PDFHub folder."""
        app = self.manager.app
        app.controller.on_open_pdfhub_folder()
    def open_in_editor(self, path):
        BannerMessage.show(self, f"Editing not yet implemented for {os.path.basename(path)}", msg_type="info")

    def add_to_split(self, path):
        """Placeholder: adds PDF to Split tab (future link)."""
        BannerMessage.show(self, f"Added to Split: {os.path.basename(path)}", msg_type="success")

    def add_to_merge(self, path):
        """Placeholder: adds PDF to Merge tab (future link)."""
        BannerMessage.show(self, f"Added to Merge: {os.path.basename(path)}", msg_type="success")


