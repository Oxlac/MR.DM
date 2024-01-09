
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

Builder.load_string(
    """
<NewAccountPopupContent>:
    orientation: "vertical"
    spacing: "30dp"
    padding: "30dp"
    size_hint_y: None
    height: self.minimum_height
    MDTextField:
        id: username
        hint_text: "Enter Username"
        text: ""
        helper_text: "Enter the username of the account"
        pos_hint: {"center_x": 0.5}
        required: True
        mode: "fill"
        multiline: False
    MDTextField:
        id: password
        hint_text: "Enter Password"
        text: ""
        helper_text: "Enter the password of the account"
        pos_hint: {"center_x": 0.5}
        required: True
        password: True
        mode: "fill"
        multiline: False
    """
)


class NewAccountPopupContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NewAccountPopup(MDDialog):
    content_cls: NewAccountPopupContent = None

    ok_button: MDRaisedButton = None

    cancel_button: MDFlatButton = None

    def __init__(self, **kwargs):
        self.content_cls = NewAccountPopupContent()
        self.ok_button = MDRaisedButton(text="Add Account")
        self.cancel_button = MDFlatButton(text="Cancel")
        self.cancel_button.bind(on_release=self.dismiss)
        super().__init__(
            title="Add New Account",
            type="custom",
            content_cls=NewAccountPopupContent(),
            buttons=[self.cancel_button, self.ok_button],
        )
