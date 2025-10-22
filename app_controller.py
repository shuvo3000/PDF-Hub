# ==========================================================
# app_controller.py
# ==========================================================
# Manages app-wide operations:
#   • Folder creation
#   • File picker
#   • Recent file tracking
#   • Banner notifications
# ==========================================================

import os
import json
import subprocess
from kivy.utils import platform
from plyer import filechooser
from ui.components.banner_message import BannerMessage


class AppController:
    """App-level controller shared by all screens."""

    def __init__(self, app):
        self.app = app
        self.user_pdf_dir = None
        self.recent_file_path = None

    # ------------------------------------------------------
    # Folder Setup
    # ------------------------------------------------------
    def ensure_pdfhub_folder(self):
        """Create ~/Documents/PDFHub folder if missing."""
        try:
            if platform == "win":
                base = os.path.join(os.path.expanduser("~"), "Documents")
            elif platform in ("android", "ios"):
                base = os.path.join(os.path.expanduser("~"), "Documents")
            else:
                base = os.path.expanduser("~")

            self.user_pdf_dir = os.path.join(base, "PDFHub")
            os.makedirs(self.user_pdf_dir, exist_ok=True)

            # Create recent.json if missing
            self.recent_file_path = os.path.join(self.user_pdf_dir, "recent.json")
            if not os.path.exists(self.recent_file_path):
                with open(self.recent_file_path, "w") as f:
                    json.dump([], f)

            BannerMessage.show(self.app.root, "📁 PDFHub folder ready", msg_type="info")

        except Exception as e:
            BannerMessage.show(self.app.root, f"Error creating folder: {e}", msg_type="error")

    # ------------------------------------------------------
    # File Picker
    # ------------------------------------------------------
    def on_open_pdf_file(self):
        """Open system file picker for PDF files."""
        try:
            paths = filechooser.open_file(title="Select a PDF", filters=[("PDF files", "*.pdf")])
            if not paths:
                BannerMessage.show(self.app.root, "No file selected.", msg_type="info")
                return
            selected = paths[0]
            BannerMessage.show(self.app.root, f"Opened: {os.path.basename(selected)}", msg_type="success")
            self.update_recent_list(selected)
        except Exception as e:
            BannerMessage.show(self.app.root, f"Error opening file: {e}", msg_type="error")

    # ------------------------------------------------------
    # Open Folder
    # ------------------------------------------------------
    def on_open_pdfhub_folder(self):
        """Open user's PDFHub folder in system file explorer."""
        try:
            if platform == "win":
                os.startfile(self.user_pdf_dir)
            elif platform == "macosx":
                subprocess.call(["open", self.user_pdf_dir])
            elif platform == "linux":
                subprocess.call(["xdg-open", self.user_pdf_dir])
            else:
                BannerMessage.show(self.app.root, "Folder open not supported on mobile.", msg_type="info")
        except Exception as e:
            BannerMessage.show(self.app.root, f"Error opening folder: {e}", msg_type="error")

    # ------------------------------------------------------
    # Recent Files Management
    # ------------------------------------------------------
    def load_recent_files(self):
        """Return up to 5 most recent files."""
        try:
            if not os.path.exists(self.recent_file_path):
                return []
            with open(self.recent_file_path, "r") as f:
                data = json.load(f)
            return data[-5:]
        except Exception as e:
            BannerMessage.show(self.app.root, f"Error loading recent files: {e}", msg_type="error")
            return []

    def update_recent_list(self, file_path):
        """Add a new file to recent.json."""
        try:
            with open(self.recent_file_path, "r") as f:
                data = json.load(f)

            if file_path not in data:
                data.append(file_path)
                data = data[-5:]
                with open(self.recent_file_path, "w") as f:
                    json.dump(data, f, indent=2)

            BannerMessage.show(self.app.root, "✅ Recent list updated", msg_type="success")
        except Exception as e:
            BannerMessage.show(self.app.root, f"Error updating recent list: {e}", msg_type="error")
