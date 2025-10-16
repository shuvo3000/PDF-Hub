from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file("ui/main.kv")

# --- Define Screens ---
class HomeScreen(Screen):
    pass

class EditScreen(Screen):
    pass

class SplitScreen(Screen):
    pass

class MergeScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass


# --- Main Layout ---
class PDFhubRoot(BoxLayout):
    def switch_tab(self, tab_name):
        """Switch main area content when user taps a bottom icon"""
        screen_manager = self.ids.screen_manager
        screen_manager.current = tab_name


# --- App ---
class PDFhubApp(App):
    def build(self):
        self.title = "PDFhub"
        return PDFhubRoot()


if __name__ == "__main__":
    PDFhubApp().run()
