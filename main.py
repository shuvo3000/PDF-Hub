
# ==========================================================
# main.py
# ==========================================================
# Entry point for PDFhub
# Handles:
#   • App initialization
#   • ScreenManager setup
#   • Loads KV and controller
# ==========================================================

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

# Import controller and screens
from app_controller import AppController
from ui.screens.home_screen import HomeScreen
from ui.screens.split_screen import SplitScreen
from ui.screens.merge_screen import MergeScreen
from ui.screens.edit_screen import EditScreen
from ui.screens.settings_screen import SettingsScreen

# Load KV layout
Builder.load_file("ui/main.kv")


class PDFhubRoot(BoxLayout):
    """
    Root container with bottom navigation and ScreenManager.
    Screen switching handled by controller methods.
    """

    def switch_tab(self, tab_name):
        """Switch to a specific tab."""
        self.ids.screen_manager.current = tab_name


class PDFhubApp(App):
    """Main application controller for PDFhub."""

    def build(self):
        self.title = "PDFhub"
        self.controller = AppController(app=self)
        root = PDFhubRoot()
        # Return first — so self.root exists
        self.root = root
        # Now safe to create folder and show banner
        self.controller.ensure_pdfhub_folder()
        return root




if __name__ == "__main__":
    PDFhubApp().run()

# # ==========================================================
# #                    PDFhub: Main Application
# # ==========================================================
# # Handles:
# #   • Navigation between Home, Edit, Split, Merge, and Settings screens
# #   • PDF splitting and merging logic
# #   • Folder creation and file picker (Home tab)
# #   • Banner notifications (success/error/info)
# # ==========================================================

# # --------------------------
# # Kivy imports
# # --------------------------
# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.checkbox import CheckBox
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.image import Image
# from kivy.uix.behaviors import DragBehavior
# from kivy.properties import ObjectProperty
# from kivy.utils import platform

# # --------------------------
# # Python stdlib imports
# # --------------------------
# import os
# import json
# import subprocess

# # --------------------------
# # Third-party imports
# # --------------------------
# from PyPDF2 import PdfReader
# from plyer import filechooser

# # --------------------------
# # Project-specific imports
# # --------------------------
# from pdf_engine.pdf_splitter import PDFSplitter
# from pdf_engine.pdf_merger import PDFMerger
# from ui.components.banner_message import BannerMessage
# from ui.components.draggable_row import DraggableRow

# # Load Kivy UI layout
# Builder.load_file("ui/main.kv")


# # ==========================================================
# #                    SCREEN DEFINITIONS
# # ==========================================================

# # --------------------------
# # HOME SCREEN
# # --------------------------
# class HomeScreen(Screen):
#     """Displays branding, recent files, and quick-access buttons."""
#     pass


# # --------------------------
# # EDIT SCREEN (Placeholder)
# # --------------------------
# class EditScreen(Screen):
#     """Reserved for future PDF editing/signature features."""
#     pass


# # --------------------------
# # SPLIT SCREEN
# # --------------------------
# class SplitScreen(Screen):
#     """Displays PDFs and allows users to split them by page number."""

#     def on_pre_enter(self):
#         """Load sample PDFs dynamically when entering Split tab."""
#         from kivy.graphics import Color, Rectangle, Line

#         # Clear existing grid
#         self.ids.split_grid.clear_widgets()

#         folder = "assets/samples"
#         os.makedirs(folder, exist_ok=True)

#         pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
#         if not pdf_files:
#             self.ids.split_grid.add_widget(
#                 Label(
#                     text="No PDF files found in assets/samples",
#                     color=(0.2, 0.2, 0.2, 1),
#                     font_size=16,
#                 )
#             )
#             return

#         # Build rows for each PDF
#         for i, pdf_file in enumerate(pdf_files):
#             file_path = os.path.join(folder, pdf_file)
#             try:
#                 reader = PdfReader(file_path)
#                 num_pages = len(reader.pages)
#             except Exception as e:
#                 num_pages = 0
#                 print(f"⚠️ Could not read {pdf_file}: {e}")

#             row = GridLayout(cols=4, size_hint_y=None, height=60, padding=[10, 5], spacing=15)

#             # Alternate row background
#             with row.canvas.before:
#                 Color(rgba=(0.97, 0.97, 0.97, 1) if i % 2 == 0 else (0.93, 0.93, 0.93, 1))
#                 row.rect = Rectangle(pos=row.pos, size=row.size)
#             row.bind(pos=lambda i, _: setattr(row.rect, "pos", i.pos),
#                      size=lambda i, _: setattr(row.rect, "size", i.size))

#             # Divider line
#             with row.canvas.after:
#                 Color(0.85, 0.85, 0.85, 1)
#                 row.line = Line(points=[row.x, row.y, row.x + row.width, row.y], width=1)
#             row.bind(pos=lambda i, _: setattr(row.line, "points", [i.x, i.y, i.x + i.width, i.y]),
#                      size=lambda i, _: setattr(row.line, "points", [i.x, i.y, i.x + i.width, i.y]))

#             # Add widgets per column
#             checkbox = CheckBox(size_hint_x=None, width=35)
#             checkbox.background_checkbox_normal = "assets/icons/checkbox_off.png"
#             checkbox.background_checkbox_down = "assets/icons/checkbox_on.png"

#             pdf_icon = Image(source="assets/icons/pdf_icon.png", size_hint_x=None, width=28)
#             label_text = f"{pdf_file} ({num_pages} pages)" if num_pages else f"{pdf_file} (Unreadable)"
#             label = Label(text=label_text, color=(0.1, 0.1, 0.1, 1),
#                           halign="left", valign="middle", text_size=(400, None), font_size=15)

#             textbox = TextInput(
#                 hint_text=f"1–{num_pages}" if num_pages else "Page #",
#                 size_hint_x=None, width=100,
#                 background_color=(1, 1, 1, 1),
#                 foreground_color=(0, 0, 0, 1),
#                 font_size=14, halign="center", input_filter="int"
#             )
#             textbox.max_page = num_pages

#             # Add to layout
#             row.add_widget(checkbox)
#             row.add_widget(pdf_icon)
#             row.add_widget(label)
#             row.add_widget(textbox)
#             self.ids.split_grid.add_widget(row)

#     def process_split(self):
#         """Perform PDF split on selected rows."""
#         if not hasattr(self.ids, "split_grid"):
#             print("⚠️ split_grid not found in layout")
#             return

#         any_selected = False

#         for row in self.ids.split_grid.children:
#             widgets = row.children[::-1]  # Reverse order
#             checkbox, pdf_icon, label, textbox = widgets[0], widgets[1], widgets[2], widgets[3]

#             if checkbox.active:
#                 any_selected = True
#                 file_name = label.text.split(" (")[0]
#                 file_path = os.path.join("assets/samples", file_name)
#                 try:
#                     # Validate page number
#                     if not textbox.text.strip():
#                         raise ValueError("Please enter a page number before splitting.")
#                     page_num = int(textbox.text.strip())
#                     max_page = getattr(textbox, "max_page", 0)
#                     if page_num <= 0 or page_num >= max_page:
#                         raise ValueError(f"Page number must be between 1 and {max_page - 1}.")

#                     # Split file
#                     splitter = PDFSplitter(file_path)
#                     splitter.split(page_num)
#                     BannerMessage.show(self, "✅ PDF split completed successfully!", msg_type="success")
#                 except ValueError as ve:
#                     BannerMessage.show(self, str(ve), msg_type="error")
#                 except Exception as e:
#                     BannerMessage.show(self, f"Error splitting {file_name}: {e}", msg_type="error")

#         if not any_selected:
#             BannerMessage.show(self, "⚠️ Please select at least one PDF to split.", msg_type="error")


# # --------------------------
# # MERGE SCREEN
# # --------------------------
# class MergeScreen(Screen):
#     """Displays draggable list of PDFs to merge."""

#     def on_pre_enter(self):
#         """Load sample PDFs dynamically."""
#         self.ids.merge_list.clear_widgets()

#         folder = "assets/samples"
#         os.makedirs(folder, exist_ok=True)
#         pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]

#         if not pdf_files:
#             BannerMessage.show(self, "No sample PDFs found in assets/samples.", msg_type="error")
#             return

#         for file_name in pdf_files:
#             file_path = os.path.join(folder, file_name)
#             try:
#                 reader = PdfReader(file_path)
#                 num_pages = len(reader.pages)
#             except Exception as e:
#                 num_pages = 0
#                 print(f"⚠️ Error reading {file_name}: {e}")

#             row = DraggableRow()
#             row.file_path = file_path
#             row.add_widget(Image(source="assets/icons/pdf_icon.png", size_hint_x=None, width=30))
#             row.add_widget(Label(
#                 text=f"{file_name} ({num_pages} pages)",
#                 halign="left", valign="middle", color=(0, 0, 0, 1)
#             ))
#             handle_btn = Image(source="assets/icons/drag_handle.png", size_hint_x=None, width=28)
#             row.handle = handle_btn
#             row.add_widget(handle_btn)

#             remove_btn = Button(
#                 background_normal="assets/icons/delete.png",
#                 background_down="assets/icons/delete.png",
#                 size_hint_x=None, width=32, background_color=(1, 0, 0, 0.1)
#             )
#             remove_btn.bind(on_press=lambda btn, r=row: self.remove_row(r))
#             row.add_widget(remove_btn)
#             self.ids.merge_list.add_widget(row)

#         self.ids.merge_btn.disabled = len(pdf_files) < 2

#     def remove_row(self, row):
#         """Remove selected PDF row."""
#         self.ids.merge_list.remove_widget(row)
#         BannerMessage.show(self, "Removed PDF from merge list.", msg_type="info")
#         self.ids.merge_btn.disabled = len(self.ids.merge_list.children) < 2

#     def on_enter(self):
#         """Bind merge button."""
#         self.ids.merge_btn.bind(on_press=lambda instance: self.merge_pdfs())

#     def merge_pdfs(self):
#         """Combine all selected PDFs."""
#         file_paths = [r.file_path for r in reversed(self.ids.merge_list.children)]
#         if len(file_paths) < 2:
#             BannerMessage.show(self, "⚠️ Select at least two PDFs to merge.", msg_type="error")
#             return

#         try:
#             merger = PDFMerger(file_paths)
#             output_path = merger.merge()
#             BannerMessage.show(self, f"✅ PDFs merged successfully!\nSaved at: {output_path}", msg_type="success")
#         except Exception as e:
#             BannerMessage.show(self, f"❌ Merge failed: {e}", msg_type="error")

#     def on_touch_up(self, touch):
#         """Handle row reordering."""
#         container = self.ids.merge_list
#         rows = list(container.children)
#         for row in rows:
#             if row.collide_point(*touch.pos):
#                 dragged = [r for r in rows if getattr(r, 'dragging', False)]
#                 if dragged:
#                     dragged_row = dragged[0]
#                     container.remove_widget(dragged_row)
#                     insert_index = rows.index(row)
#                     container.add_widget(dragged_row, index=insert_index)
#                     BannerMessage.show(self, "✅ Files reordered successfully.", msg_type="info")
#                     break
#         for r in rows:
#             if hasattr(r, 'dragging'):
#                 r.dragging = False
#         return super().on_touch_up(touch)


# # --------------------------
# # SETTINGS SCREEN (Placeholder)
# # --------------------------
# class SettingsScreen(Screen):
#     pass


# # --------------------------
# # DRAGGABLE ROW (Merge helper)
# # --------------------------
# class DraggableRow(DragBehavior, BoxLayout):
#     """Each row in Merge tab can be dragged to reorder."""
#     file_path = ObjectProperty(None)

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.drag_timeout = 100000
#         self.drag_distance = 10
#         self.size_hint_y = None
#         self.height = 50
#         self.spacing = 10
#         self.padding = 5
#         self.dragging = False

#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             self.dragging = True
#         return super().on_touch_down(touch)


# # ==========================================================
# #                   ROOT LAYOUT CLASS
# # ==========================================================
# class PDFhubRoot(BoxLayout):
#     """Root container managing bottom navigation and screen switching."""

#     def switch_tab(self, tab_name):
#         """Switch between screens."""
#         screen_manager = self.ids.screen_manager
#         print(f"🔄 Switching to tab: {tab_name}")
#         screen_manager.current = tab_name


# # ==========================================================
# #                   MAIN APP CLASS
# # ==========================================================
# class PDFhubApp(App):
#     """Main application controller."""

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.user_pdf_dir = None
#         self.recent_file_path = None

#     def build(self):
#         """Initialize and build UI."""
#         self.title = "PDFhub"
#         self.root = PDFhubRoot()
#         self.ensure_pdfhub_folder()
#         self.load_recent_files()
#         return self.root

#     # ------------------------------------------------------
#     # Ensure Documents/PDFHub exists
#     # ------------------------------------------------------
#     def ensure_pdfhub_folder(self):
#         """Create Documents/PDFHub folder if missing."""
#         try:
#             if platform == "win":
#                 base = os.path.join(os.path.expanduser("~"), "Documents")
#             elif platform in ("android", "ios"):
#                 base = os.path.join(os.path.expanduser("~"), "Documents")
#             else:
#                 base = os.path.expanduser("~")

#             self.user_pdf_dir = os.path.join(base, "PDFHub")
#             os.makedirs(self.user_pdf_dir, exist_ok=True)

#             self.recent_file_path = os.path.join(self.user_pdf_dir, "recent.json")
#             if not os.path.exists(self.recent_file_path):
#                 with open(self.recent_file_path, "w") as f:
#                     json.dump([], f)

#             BannerMessage.show(self.root, "📁 PDFHub folder ready")

#         except Exception as e:
#             BannerMessage.show(self.root, f"Error creating folder: {e}")

#     # ------------------------------------------------------
#     # Load recent files
#     # ------------------------------------------------------
#     def load_recent_files(self):
#         """Load 5 most recent PDF paths."""
#         try:
#             if not self.recent_file_path or not os.path.exists(self.recent_file_path):
#                 return []
#             with open(self.recent_file_path, "r") as f:
#                 data = json.load(f)
#             return data[-5:]
#         except Exception as e:
#             BannerMessage.show(self.root, f"Error loading recent files: {e}")
#             return []

#     # ------------------------------------------------------
#     # File picker
#     # ------------------------------------------------------
#     def on_open_pdf_file(self):
#         """Open system file picker for PDFs."""
#         try:
#             paths = filechooser.open_file(title="Select a PDF", filters=[("PDF files", "*.pdf")])
#             if not paths:
#                 BannerMessage.show(self.root, "No file selected.")
#                 return
#             selected = paths[0]
#             BannerMessage.show(self.root, f"Opened: {os.path.basename(selected)}")
#             self.update_recent_list(selected)
#         except Exception as e:
#             BannerMessage.show(self.root, f"Error opening file: {e}")

#     # ------------------------------------------------------
#     # Open PDFHub folder
#     # ------------------------------------------------------
#     def on_open_pdfhub_folder(self):
#         """Open user's PDFHub folder in file explorer."""
#         try:
#             if platform == "win":
#                 os.startfile(self.user_pdf_dir)
#             elif platform == "macosx":
#                 subprocess.call(["open", self.user_pdf_dir])
#             elif platform == "linux":
#                 subprocess.call(["xdg-open", self.user_pdf_dir])
#             else:
#                 BannerMessage.show(self.root, "Folder open not supported on mobile.")
#         except Exception as e:
#             BannerMessage.show(self.root, f"Error opening folder: {e}")

#     # ------------------------------------------------------
#     # Update recent.json
#     # ------------------------------------------------------
#     def update_recent_list(self, file_path):
#         """Append new file to recent.json (keep last 5)."""
#         try:
#             with open(self.recent_file_path, "r") as f:
#                 data = json.load(f)

#             if file_path not in data:
#                 data.append(file_path)
#                 data = data[-5:]
#                 with open(self.recent_file_path, "w") as f:
#                     json.dump(data, f, indent=2)

#             BannerMessage.show(self.root, "✅ Recent list updated")
#         except Exception as e:
#             BannerMessage.show(self.root, f"Error updating recent list: {e}")


# # ==========================================================
# #                   APP EXECUTION
# # ==========================================================
# if __name__ == "__main__":
#     PDFhubApp().run()
