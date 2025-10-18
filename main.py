# -----------------------------
# PDFhub: Main Application File
# -----------------------------
# This file handles:
# - Screen navigation (Home, Edit, Split, Merge, Settings)
# - Dynamic PDF grid rendering
# - PDF splitting logic integration with PDFSplitter class
# - Popup notifications for user actions

# --- Import core Kivy components ---
from kivy.app import App                          # Base class for all Kivy apps
from kivy.lang import Builder                     # Loads .kv files for UI structure
from kivy.uix.boxlayout import BoxLayout          # Main layout for app container
from kivy.uix.screenmanager import ScreenManager, Screen  # Manages multiple screens/tabs
from kivy.uix.gridlayout import GridLayout        # For displaying PDFs in grid format
from kivy.uix.checkbox import CheckBox            # Checkbox widget for file selection
from kivy.uix.textinput import TextInput          # Text box for entering split page
from kivy.uix.button import Button                # Buttons for actions
from kivy.uix.label import Label                  # Label for displaying text
from kivy.uix.popup import Popup                  # Popup dialog for success/error messages
import os                                         # Used for working with local file paths
from pdf_engine.pdf_splitter import PDFSplitter   # Custom class handling PDF splitting logic

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
        """Build the grid dynamically when entering the Split tab (modern design)."""
        from kivy.graphics import Color, Rectangle, Line
        from kivy.uix.image import Image

        self.ids.split_grid.clear_widgets()

        folder = "assets/samples"
        if not os.path.exists(folder):
            os.makedirs(folder)

        pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]
        if not pdf_files:
            self.ids.split_grid.add_widget(
                Label(text="No PDF files found in assets/samples",
                    color=(0.2, 0.2, 0.2, 1),
                    font_size=16)
            )
            return

        for i, pdf_file in enumerate(pdf_files):
            # Alternate gradient background (slightly different shades)
            row = GridLayout(cols=4, size_hint_y=None, height=60, padding=[10, 5], spacing=15)

            # --- Row background ---
            with row.canvas.before:
                Color(rgba=(0.97, 0.97, 0.97, 1) if i % 2 == 0 else (0.93, 0.93, 0.93, 1))
                row.rect = Rectangle(pos=row.pos, size=row.size)

            # --- Keep background responsive on resize ---
            def update_rect(instance, _):
                row.rect.pos = instance.pos
                row.rect.size = instance.size
            row.bind(pos=update_rect, size=update_rect)

            # --- Optional bottom divider line for cleaner layout ---
            with row.canvas.after:
                Color(0.85, 0.85, 0.85, 1)
                row.line = Line(points=[row.x, row.y, row.x + row.width, row.y], width=1)
            def update_line(instance, _):
                row.line.points = [instance.x, instance.y, instance.x + instance.width, instance.y]
            row.bind(pos=update_line, size=update_line)

            # --- Custom, larger checkbox ---
            checkbox = CheckBox(size_hint_x=None, width=35)
            checkbox.background_checkbox_normal = "assets/icons/checkbox_off.png"
            checkbox.background_checkbox_down = "assets/icons/checkbox_on.png"

            # --- PDF Icon (small red symbol) ---
            pdf_icon = Image(
                source="assets/icons/pdf_icon.png",
                size_hint_x=None,
                width=28,
                allow_stretch=True,
                keep_ratio=True
            )

            # --- File name label ---
            label = Label(
                text=pdf_file,
                color=(0.1, 0.1, 0.1, 1),
                halign="left",
                valign="middle",
                text_size=(400, None),
                font_size=15
            )

            # --- Page number input box ---
            textbox = TextInput(
                hint_text="Page #",
                size_hint_x=None,
                width=100,
                background_color=(1, 1, 1, 1),
                foreground_color=(0, 0, 0, 1),
                font_size=14,
                halign="center"
            )

            # Add all widgets in order
            row.add_widget(checkbox)
            row.add_widget(pdf_icon)
            row.add_widget(label)
            row.add_widget(textbox)
            self.ids.split_grid.add_widget(row)

    def process_split(self):
        """Handle the split action for selected PDFs."""
        if not hasattr(self.ids, "split_grid"):
            print("⚠️ split_grid not found in layout")
            return

        any_selected = False

        # Loop through all rows
        for row in self.ids.split_grid.children:
            # row.children order is reversed (last added is first)
            widgets = row.children[::-1]

            # We expect: [checkbox, pdf_icon, label, textbox]
            checkbox = widgets[0]
            label = widgets[2]   # skip pdf_icon
            textbox = widgets[3]

            if checkbox.active:
                any_selected = True
                file_path = os.path.join("assets/samples", label.text)

                try:
                    # Validate the entered page number
                    page_num = int(textbox.text.strip())
                    splitter = PDFSplitter(file_path)
                    part1, part2 = splitter.split(page_num)
                    self.show_popup(
                        f"✅ Split complete!\n\nSaved in:\n{os.path.dirname(part1)}"
                    )
                except ValueError:
                    self.show_popup(
                        f"⚠️ Please enter a valid page number for {label.text}."
                    )
                except Exception as e:
                    self.show_popup(f"⚠️ Error splitting {label.text}\n{e}")

        if not any_selected:
            self.show_popup("⚠️ Please select at least one PDF to split.")



    def show_popup(self, message):
        """Displays a popup message box with the given text."""
        popup = Popup(
            title="PDFhub",
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()


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
