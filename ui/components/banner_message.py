from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle


class BannerMessage(BoxLayout):
    """
    A reusable professional banner notification that slides down from the top.
    Used for showing success, error, or info messages in any screen.

    Example:
        BannerMessage.show(self, "✅ Split complete!", msg_type="success")
    """

    # Predefined message colors (RGBA)
    COLORS = {
        "error": (0.9, 0.2, 0.2, 1),      # red
        "success": (0.1, 0.7, 0.2, 1),    # green
        "info": (0.2, 0.5, 0.9, 1),       # blue
    }

    def __init__(self, message, msg_type="info", duration=4, **kwargs):
        """
        Create a banner with text and color style.
        - message: text to show
        - msg_type: one of ("error", "success", "info")
        - duration: how many seconds to stay visible
        """
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50
        self.opacity = 0  # start hidden
        self.orientation = "vertical"
        self.pos_hint = {"top": 1.05}  # starts slightly above the screen
        self.spacing = 10
        self.padding = [10, 8]

        # Choose background color based on type
        color = self.COLORS.get(msg_type, self.COLORS["info"])

        # --- Background setup ---
        with self.canvas.before:
            self.bg_color = Color(*color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

        # --- Label setup ---
        self.label = Label(
            text=message,
            color=(1, 1, 1, 1),  # white text
            font_size=16,
            halign="center",
            valign="middle"
        )
        self.add_widget(self.label)

        # --- Slide down animation (entry) ---
        Animation(opacity=1, pos_hint={"top": 0.98}, d=0.35, t="out_quad").start(self)

        # --- Schedule fade-out and removal ---
        Clock.schedule_once(lambda dt: self.dismiss(), duration)

    # Keep background rectangle synced with widget position
    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # Animate disappearance
    def dismiss(self):
        anim = Animation(opacity=0, pos_hint={"top": 1.05}, d=0.35, t="in_quad")
        anim.bind(on_complete=lambda *_: self.parent.remove_widget(self))
        anim.start(self)

    # --- Static method to make usage easy ---
    @staticmethod
    def show(parent, message, msg_type="info", duration=4):
        """
        Display a banner message on the given parent widget.
        Example:
            BannerMessage.show(self, "✅ Done!", msg_type="success")
        """
        banner = BannerMessage(message, msg_type=msg_type, duration=duration)
        parent.add_widget(banner, index=0)
