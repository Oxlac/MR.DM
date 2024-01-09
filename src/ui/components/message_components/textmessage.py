from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard

Builder.load_string(
    """
<TextMessage>:
    elevation: 2
    md_bg_color: app.theme_cls.bg_light
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height
    padding: "20dp", "20dp", "20dp", "20dp"
    spacing: "8dp"

    RelativeLayout:
        size_hint_y: None
        size_hint_x: 1
        height: "40dp"
        Label:
            text: "Text Message"
            color: app.theme_cls.primary_color
            font_size: "22sp"
            bold: True
            size_hint_y: None
            height: self.texture_size[1]
            pos_hint: {"center_y": 0.5, "center_x": .15}
        MDIcon:
            icon: "text"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            size_hint_x: None
            width: self.texture_size[1]
            pos_hint: {"center_y": 0.5, "left": 1}

        MDIconButton:
            icon: "trash-can-outline"
            pos_hint: {"center_y": 0.5, "right": 1}
            on_release: root.parent.remove_widget(root)

    MDTextField:
        id:content
        hint_text: "Enter your message here"
        mode: "rectangle"
        multiline: True
        size_hint_y: None
        height: "100dp"
        pos_hint: {"center_y": 0.5} 
    """
)


class TextMessage(MDCard):
    pass
