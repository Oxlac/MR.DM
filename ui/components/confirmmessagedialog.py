from kivy.lang import Builder

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivy.uix.boxlayout import BoxLayout

Builder.load_string(
    """
<MessageConfirmDialogContent>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    padding: "12dp"

    MDLabel:
        text: "Enter your password to confirm"
        font_style: "Caption"

    MDTextField:
        id: password
        hint_text: "Password"
        helper_text: "Enter your password to confirm"
        helper_text_mode: "persistent"
        mode: "fill"
        pos_hint: {"center_x": .5, "center_y": .5}
        password: True
        on_text: root.parent.parent.parent.enable_button()
    """
)


class MessageConfirmDialogContent(BoxLayout):
    pass


class MessageConfirmDialog(MDDialog):
    content_cls = None
    """
    Stores the content of the dialog
    """

    ok_button = None
    """
    Stores the ok button
    """

    cancel_button = None
    """
    Stores the cancel button
    """

    callback = None
    """
    Stores the callback function to be called when the user confirms the dialog
    """

    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.auto_dismiss = False
        self.content_cls = MessageConfirmDialogContent()
        self.ok_button = MDRaisedButton(text="Send Messages")
        self.cancel_button = MDFlatButton(text="Cancel")
        self.ok_button.bind(on_release=self.on_confirm)

        super().__init__(
            title="Confirm Messages",
            type="custom",
            content_cls=self.content_cls,
            buttons=[self.cancel_button, self.ok_button],
            **kwargs
        )
        self.ok_button.disabled = True

    def enable_button(self, *args):
        """
        Enables the ok button only when there is text in the password fields
        """
        if self.content_cls.ids.password.text:
            self.ok_button.disabled = False
        else:
            self.ok_button.disabled = True

    def on_confirm(self, *args):
        """
        Called when the user confirms the dialog
        """
        self.callback(self.content_cls.ids.password.text)
