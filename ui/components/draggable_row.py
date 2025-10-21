# ==========================================================
#  Draggable Row Component
#  -----------------------
#  Reusable Kivy widget that allows dragging a BoxLayout
#  to reorder PDF items in the Merge list.
# ==========================================================

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.properties import ObjectProperty, BooleanProperty


class DraggableRow(DragBehavior, BoxLayout):
    """
    Represents a single draggable row in the Merge screen.
    The user can drag this row (using a handle icon) to
    reorder the PDF list visually.
    """

    # Store the file path linked to this row
    file_path = ObjectProperty(None)

    # Track whether this row is currently being dragged
    is_dragged = BooleanProperty(False)

    def __init__(self, **kwargs):
        """
        Initialize row behavior and appearance.
        """
        super().__init__(**kwargs)

        # --- Configure drag behavior ---
        self.drag_distance = 5       # Start drag after 5px movement
        self.drag_timeout = 999999   # Disable long-press delay
        self.size_hint_y = None      # Fixed row height
        self.height = 50
        self.spacing = 10
        self.padding = 5
        self.handle = None           # Will hold the drag handle widget

    # ------------------------------------------------------
    #                 TOUCH BEHAVIOR EVENTS
    # ------------------------------------------------------
    def on_touch_down(self, touch):
        """
        Start dragging only when the user presses the handle icon.
        """
        if self.handle and self.handle.collide_point(*touch.pos):
            self.is_dragged = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """
        Stop dragging when the user releases the mouse/finger.
        """
        self.is_dragged = False
        return super().on_touch_up(touch)
