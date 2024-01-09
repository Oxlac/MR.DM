from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog

Builder.load_string(
    """
<HashtagDialog>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        id: hashtags
        hint_text: "Enter Hashtags"
        helper_text: "Seperate Hashtags with a comma without a space in middle"
        text: "oxlac,oxlacofficial"
    MDTextField:
        id: limit
        hint_text: "Enter Limit of Posts"
        helper_text: "Enter a number between 1 and 100"
        text: "10"
    """
)


class HashtagDialogContent(BoxLayout):
    pass


class HashtagDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
