from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import MDCard

Builder.load_string(
    """
<UserCard>:
    orientation: "horizontal"
    size_hint_y: None
    height: "80dp"
    padding: "10dp"
    spacing: "20dp"

    AsyncImage:
        id: profile_pic
        canvas:
            Clear:
            Color:
                rgb: 1, 1, 1
            Ellipse:
                pos: self.pos
                size: self.size
                texture: self.texture
        source: root.profile_pic_url
        size_hint:None, None
        size: "50dp", "50dp"
        pos_hint: {"center_y": 0.5}

    BoxLayout:
        orientation: "vertical"
        size_hint_x: 0.7

        MDLabel:
            text: "@"+root.username
            font_size: "18sp"
            halign: "left"
            valign: "center"
            pos_hint: {"center_y": 0.5}
        MDLabel:
            text: str(root.userid)
            font_size: "12sp"
            halign: "left"
            valign: "center"
            font_style: "Caption"
            pos_hint: {"center_y": 0.5}

    MDIconButton:
        icon: "delete"
        pos_hint: {"center_y": 0.5}
        on_release: root.delete_callback(root)
        color: 1, 0, 0, 1
        
    """
)


class UserCard(MDCard, ButtonBehavior):
    """
    Represents an user card on the welcome screen.
    Displays data such as username, last active and profile picture
    """

    username: StringProperty = StringProperty()

    profile_pic_url: StringProperty = StringProperty()

    userid: NumericProperty = NumericProperty()

    delete_callback = None

    def __init__(self, username, profile_pic_url, userid, delete_callback, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.profile_pic_url = profile_pic_url
        self.userid = userid
        self.delete_callback = delete_callback
