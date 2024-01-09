from kivy.lang import Builder
from kivymd.uix.card import MDCard

Builder.load_string(
    """
<MessageProgress>:
    orientation: "vertical"
    size_hint_y: None
    height: "100dp"
    padding: "10dp"
    spacing: "10dp"
    MDLabel:
        text: "Sending messages..."
        halign: "center"
        font_style: "H6"
    MDSpinner:
        size_hint: None, None
        size: "32dp", "32dp"
        color: app.theme_cls.primary_color
        active: True
"""
)


class MessageProgress(MDCard):
    pass
