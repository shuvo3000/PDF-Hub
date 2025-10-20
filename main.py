# -----------------------------
# PDFhub: Main Application File
# -----------------------------
# This file handles:
# - Screen navigation (Home, Edit, Split, Merge, Settings)
# - Dynamic PDF grid rendering
# - PDF splitting logic integration with PDFSplitter class
# - Popup notifications for user actions

# --- Import core Kivy components ---
from kivy.app import App                                    # Base class for all Kivy apps
from kivy.lang import Builder                               # Loads .kv files for UI structure
from kivy.uix.boxlayout import BoxLayout                    # Main layout for app container
from kivy.uix.screenmanager import ScreenManager, Screen    # Manages multiple screens/tabs
from kivy.uix.gridlayout import GridLayout                  # For displaying PDFs in grid format
from kivy.uix.checkbox import CheckBox                      # Checkbox widget for file selection
from kivy.uix.textinput import TextInput                    # Text box for entering split page
from kivy.uix.button import Button                          # Buttons for actions
from kivy.uix.label import Label                            # Label for displaying text
from kivy.uix.popup import Popup                            # Popup dialog for success/error messages
import os                                                   # Used for working with local file paths
from pdf_engine.pdf_splitter import PDFSplitter             # Custom class handling PDF splitting logic
from PyPDF2 import PdfReader                                # import here so we can count pages
from ui.components.banner_message import BannerMessage    # This import is for the error and other types of message for this app    

# --- Load Kivy UI Layout ---
# This loads the structure defined in ui/main.kv
Builder.load_file("ui/main.kv")


# ==========================================================
#                   SCREEN DEFINITIONS
# ==========================================================

# --- Home Screen (Placeholder for now) ---
class HomeScreen(Screen):
    pass  # To be implemented later (file browser or recent PDFs view)


# --- Edit Screen (Placeholder for future form filling/signature feature) ---
class EditScreen(Screen):
    pass


# --- Split Screen (Handles PDF splitting UI and logic) ---
class SplitScreen(Screen):

    # Triggered each time the user opens the Split tab
    def on_pre_enter(self):
        """Builds the grid dynamically when entering the Split tab (modern design with page count)."""
        from kivy.graphics import Color, Rectangle, Line
        from kivy.uix.image import Image

        # --- Clear previous rows before rebuilding ---
        self.ids.split_grid.clear_widgets()

        folder = "assets/samples"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Get all PDF files in the folder
        pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
        if not pdf_files:
            self.ids.split_grid.add_widget(
                Label(
                    text="No PDF files found in assets/samples",
                    color=(0.2, 0.2, 0.2, 1),
                    font_size=16,
                )
            )
            return

        # Loop through each PDF and build a row for it
        for i, pdf_file in enumerate(pdf_files):
            file_path = os.path.join(folder, pdf_file)

            # --- Read total number of pages using PyPDF2 ---
            try:
                reader = PdfReader(file_path)
                num_pages = len(reader.pages)
            except Exception as e:
                num_pages = 0
                print(f"⚠️ Could not read {pdf_file}: {e}")

            # --- Create row layout ---
            row = GridLayout(
                cols=4, size_hint_y=None, height=60, padding=[10, 5], spacing=15
            )

            # --- Alternate row background for visual clarity ---
            with row.canvas.before:
                Color(
                    rgba=(0.97, 0.97, 0.97, 1)
                    if i % 2 == 0
                    else (0.93, 0.93, 0.93, 1)
                )
                row.rect = Rectangle(pos=row.pos, size=row.size)

            # Keep background responsive
            def update_rect(instance, _):
                row.rect.pos = instance.pos
                row.rect.size = instance.size

            row.bind(pos=update_rect, size=update_rect)

            # --- Optional divider line ---
            with row.canvas.after:
                Color(0.85, 0.85, 0.85, 1)
                row.line = Line(points=[row.x, row.y, row.x + row.width, row.y], width=1)

            def update_line(instance, _):
                row.line.points = [
                    instance.x,
                    instance.y,
                    instance.x + instance.width,
                    instance.y,
                ]

            row.bind(pos=update_line, size=update_line)

            # --- Checkbox (custom design) ---
            checkbox = CheckBox(size_hint_x=None, width=35)
            checkbox.background_checkbox_normal = "assets/icons/checkbox_off.png"
            checkbox.background_checkbox_down = "assets/icons/checkbox_on.png"

            # --- PDF Icon (small red symbol) ---
            pdf_icon = Image(
                source="assets/icons/pdf_icon.png",
                size_hint_x=None,
                width=28,
                allow_stretch=True,
                keep_ratio=True,
            )

            # --- Label with filename and page count ---
            label_text = (
                f"{pdf_file} ({num_pages} pages)"
                if num_pages
                else f"{pdf_file} (Unreadable)"
            )
            label = Label(
                text=label_text,
                color=(0.1, 0.1, 0.1, 1),
                halign="left",
                valign="middle",
                text_size=(400, None),
                font_size=15,
            )

            # --- Page number textbox (limits user input) ---
            textbox = TextInput(
                hint_text=f"1–{num_pages}" if num_pages else "Page #",
                size_hint_x=None,
                width=100,
                background_color=(1, 1, 1, 1),
                foreground_color=(0, 0, 0, 1),
                font_size=14,
                halign="center",
                input_filter="int",  # restricts input to numbers only
            )

            # Store max allowed page as a custom property
            textbox.max_page = num_pages

            # Add widgets to the row
            row.add_widget(checkbox)
            row.add_widget(pdf_icon)
            row.add_widget(label)
            row.add_widget(textbox)
            self.ids.split_grid.add_widget(row)

    # ======================================================
    #               PROCESS SPLIT LOGIC
    # ======================================================
    def process_split(self):
        """
        Handles splitting the selected PDFs based on user input.
        This version:
        ✅ Uses Toast messages for feedback
        ✅ Validates user input for page numbers
        ✅ Prevents invalid page numbers (e.g., 0 or beyond max pages)
        """
        from ui.components.toast import Toast   # Import toast component

        # --- Check if split_grid exists ---
        if not hasattr(self.ids, "split_grid"):
            print("⚠️ split_grid not found in layout")
            return

        any_selected = False  # Tracks if user selected at least one file

        # --- Loop through each row (PDF entry) in the grid ---
        for row in self.ids.split_grid.children:
            # row.children returns widgets in reverse order
            widgets = row.children[::-1]

            # Order: [checkbox, pdf_icon, label, textbox]
            checkbox = widgets[0]
            label = widgets[2]   # skip icon in the middle
            textbox = widgets[3]

            # Proceed only if checkbox is selected
            if checkbox.active:
                any_selected = True
                file_name = label.text.split(" (")[0]  # Extract pure file name (without page count)
                file_path = os.path.join("assets/samples", file_name)

                try:
                    # --- Validate text box input ---
                    if not textbox.text.strip():
                        raise ValueError("Please enter a page number before splitting.")

                    # Convert input to integer
                    page_num = int(textbox.text.strip())

                    # Get max page count (saved earlier during load)
                    max_page = getattr(textbox, "max_page", 0)

                    # --- Validate page number range ---
                    if page_num <= 0 or page_num >= max_page:
                        raise ValueError(f"Page number must be between 1 and {max_page - 1}.")

                    # --- Perform the split ---
                    splitter = PDFSplitter(file_path)
                    part1, part2 = splitter.split(page_num)

                    # ✅ Success toast message
                    BannerMessage.show(self, "✅ PDF split completed successfully!", msg_type="success")

                except ValueError as ve:
                    # ⚠️ Invalid user input
                    BannerMessage.show(self, f"{ve}", msg_type="error")

                except Exception as e:
                    # ⚠️ Unexpected error
                    BannerMessage.show(self, f"Error splitting {file_name}: {e}", msg_type="error")

        # --- No file was selected ---
        if not any_selected:
            BannerMessage.show(self, "⚠️ Please select at least one PDF to split.", msg_type="error")

# --- Merge Screen (Placeholder for combining multiple PDFs) ---
class MergeScreen(Screen):
    pass


# --- Settings Screen (Placeholder for app preferences or about page) ---
class SettingsScreen(Screen):
    pass


# ==========================================================
#                   MAIN APP LAYOUT
# ==========================================================

# Root layout class manages the bottom tab navigation and screen switching
class PDFhubRoot(BoxLayout):

    def switch_tab(self, tab_name):
        """Switches between Home, Edit, Split, Merge, and Settings tabs."""
        screen_manager = self.ids.screen_manager
        print(f"🔄 Switching to tab: {tab_name}")
        screen_manager.current = tab_name


# ==========================================================
#                   MAIN APP INITIALIZER
# ==========================================================

class PDFhubApp(App):
    """Main entry point for the Kivy application."""

    def build(self):
        # Set the app window title
        self.title = "PDFhub"

        # Load the main layout
        return PDFhubRoot()


# ==========================================================
#                   APP EXECUTION
# ==========================================================

# Launch the Kivy app
if __name__ == "__main__":
    PDFhubApp().run()
