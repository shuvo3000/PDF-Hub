# --- Kivy imports for the widget, animation, timing, and drawing ---
from kivy.uix.relativelayout import RelativeLayout          # container for the toast bar
from kivy.uix.label import Label                             # to show the message text
from kivy.animation import Animation                         # slide / fade animations
from kivy.clock import Clock                                 # schedule animations
from kivy.graphics import Color, RoundedRectangle            # colored rounded background


class Toast(RelativeLayout):
    """Animated top banner (toast) that styles itself by message type."""

    # ---------- Theme colors (opaque so text always contrasts) ----------
    ERROR_COLOR   = (0.85, 0.10, 0.10, 1)    # red
    SUCCESS_COLOR = (0.00, 0.60, 0.20, 1)    # green
    INFO_COLOR    = (0.10, 0.40, 0.90, 1)    # blue

    def __init__(self, message: str, msg_type: str = "info", **kwargs):
        # initialize the base RelativeLayout
        super().__init__(**kwargs)

        # ---------- Sizing and starting position ----------
        self.size_hint = (1, None)                  # full width, fixed height
        self.pos_hint  = {"top": 1.05}              # start just above the window
        self.opacity   = 1                          # fully opaque (we’ll fade later)

        # choose background color from msg_type
        bg = (self.ERROR_COLOR   if msg_type == "error"   else
              self.SUCCESS_COLOR if msg_type == "success" else
              self.INFO_COLOR)

        # Force text color to black so message is always readable on light backgrounds
        text_color = (0, 0, 0, 1)

        # estimate a comfortable height from message length (multi-line support)
        est_lines = max(1, len(message) // 55 + 1)  # rough chars per line
        self.height = max(55, est_lines * 28)       # at least 55px high

        # ---------- Colored rounded background (drawn behind children) ----------
        with self.canvas.before:                    # background must be below the label
            self._bg_color = Color(*bg)             # set the fill color
            self._bg_rect  = RoundedRectangle(      # rounded bottom corners
                radius=[0, 0, 8, 8],
                pos=self.pos,                       # ensure an initial rect is drawn
                size=self.size
            )

        # keep the rounded rectangle glued to this widget’s size/pos
        def _sync_bg_rect(_inst, _val):
            self._bg_rect.pos  = self.pos
            self._bg_rect.size = self.size
        self.bind(pos=_sync_bg_rect, size=_sync_bg_rect)

        # ---------- Foreground label (the text) ----------
        self.label = Label(
            text=message,                            # the message to show
            color=text_color,                        # contrast text color (forced black)
            bold=True,                               # a bit bolder for readability
            font_size=16,                            # comfortable size
            halign="center",                         # horizontal alignment (needs text_size)
            valign="middle",                         # vertical alignment (needs text_size)
            size_hint=(1, 1),                        # fill the toast area
        )

        # IMPORTANT: halign/valign only take effect when text_size is set to the widget size.
        # At __init__ time the label's width is 0, so we BIND to size and update text_size THEN.
        def _sync_text_size(lbl, _size):
            lbl.text_size = (lbl.width - 30, lbl.height)  # add side padding visually
        self.label.bind(size=_sync_text_size)       # ensures text lays out after sizing

        # add the label on top of the background
        self.add_widget(self.label)

    # ---------- Static helper to create, animate, and auto-remove a toast ----------
    @staticmethod
    def show(parent, message: str, msg_type: str = "info", duration: float = 5.0):
        """
        Create a toast inside `parent`, slide it down, keep it visible for `duration`
        seconds, then fade it out and remove it.
        """
        toast = Toast(message, msg_type=msg_type)   # build the widget
        parent.add_widget(toast)                    # place it in the current screen
        toast.canvas.ask_update()                   # force a draw pass before anims

        # Start the slide-down on the next frame to avoid race with initial draw.
        def _start(*_):
            Animation(pos_hint={"top": 0.95}, d=0.35, t="out_quad").start(toast)

            # After `duration` seconds, fade out and remove from parent.
            def _fade_out(*_):
                anim = Animation(opacity=0, d=0.4)
                anim.bind(on_complete=lambda *_: parent.remove_widget(toast))
                anim.start(toast)

            Clock.schedule_once(_fade_out, duration)

        Clock.schedule_once(_start, 0)              # run on next frame
