import threading

from instaloader import Profile
from kivy.clock import mainthread
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from backend.session import Session

Builder.load_string(
    """
<ManualDialogContent>:
    cols: 1
    padding: dp(10)
    size_hint_y: None
    height: dp(250)
    spacing: dp(20)

    MDSegmentedControl:
        id: segmented_control
        md_bg_color: app.theme_cls.bg_normal
        segment_color: app.theme_cls.primary_color
        on_active: root.change_content(*args)

        MDSegmentedControlItem:
            id: individual
            text: "[color=fff]Individual[/color]"

        MDSegmentedControlItem:
            id: multiple
            text: "[color=fff]Multiple[/color]"
    
    BoxLayout:
        id: content
        orientation: "vertical"
        size_hint: 1, .9

        ManualDialogIndividualContent:

<ManualDialogIndividualContent>:
    cols: 1
    padding: dp(10)

    MDLabel:
        text: "Enter a single username. Click Validate to check if the username is valid"
        halign: "left"
        size_hint_y: None
        font_style: "Caption"
        height: dp(30)

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        spacing: dp(10)
        height: dp(50)

        MDTextField:
            id: username
            hint_text: "Username"
            helper_text: "Enter a single username"
            mode: "fill"
            size_hint_x: .8
            helper_text_mode: "persistent"
            multiline: False
            on_text: root.enabled_validate(self.text)

        FloatLayout:
            size_hint_x: .2
            MDRectangleFlatButton:
                id: validate
                text: "Validate"
                size_hint_x: .2
                disabled: True
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.validate_username()
                opacity: 1 if not (root.loading or root.valid) else 0

            MDSpinner:
                id: spinner
                size_hint: None, None
                size: dp(46), dp(46)
                pos_hint: {"center_x": .5, "center_y": .5}
                active: root.loading

            MDIcon:
                id: valid_icon
                icon: "check"
                size_hint: None, None
                size: dp(46), dp(46)
                pos_hint: {"center_x": .5, "center_y": .5}
                color: 0, 1, 0, 1
                opacity: 1 if root.valid else 0

<ManualDialogMultipleContent>:
    cols: 1
    padding: dp(20)
    spacing: dp(20)

    MDLabel:
        text: "Enter multiple usernames separated by a comma. Click Validate to check if the usernames are valid. If you are entering large amounts of usernames, it is recommended to use the CSV import feature"
        halign: "left"
        valign: "center"
        size_hint_y: None
        font_style: "Caption"
        height: dp(30)

    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        spacing: dp(10)
        height: dp(50)

        MDTextField:
            id: usernames
            hint_text: "Usernames"
            helper_text: "Enter multiple usernames separated by a comma"
            mode: "rectangle"
            size_hint_x: .8
            helper_text_mode: "persistent"
            multiline: True
            on_text: root.enabled_validate(self.text)

        FloatLayout:
            size_hint_x: .2
            MDRectangleFlatButton:
                id: validate
                text: "Validate"
                size_hint_x: .2
                disabled: True
                pos_hint: {"center_x": .5, "center_y": .5}
                on_release: root.validate_username()
                opacity: 1 if not (root.loading or root.valid) else 0

            MDSpinner:
                id: spinner
                size_hint: None, None
                size: dp(46), dp(46)
                pos_hint: {"center_x": .5, "center_y": .5}
                active: root.loading

            MDIcon:
                id: valid_icon
                icon: "check"
                size_hint: None, None
                size: dp(46), dp(46)
                pos_hint: {"center_x": .5, "center_y": .5}
                color: 0, 1, 0, 1
                opacity: 1 if root.valid else 0    
    """
)


class ManualDialogIndividualContent(GridLayout):
    session = None
    """
    The backend session
    """

    valid = BooleanProperty(False)
    """
    Whether the username is valid
    """

    loading = BooleanProperty(False)
    """
    Whether the username is being validated
    """

    verified_username = []
    """
    The usernames that have been verified
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = Session()

    def enabled_validate(self, text):
        """
        Enables the validate button if there is text in the username field
        """
        self.ids.validate.disabled = text == ""
        # Reset the valid icon and the add button and the verified usernames
        if self.valid:
            self.valid = False
            self.parent.parent.parent.parent.children[0].children[0].children[
                0
            ].disabled = True
            self.verified_username = []

    def validate_username(self):
        """
        Validates the username
        """
        self.loading = True
        threading.Thread(target=self._validate_username).start()

    def _validate_username(self):
        """
        Validates the username on a separate thread
        """
        username = self.ids.username.text.strip()
        try:
            Profile.from_username(self.session.loader.context, username)
            self.set_valid(True)
            self.verified_username.append(username)
        except Exception:
            self.set_valid(False)
        self.set_loading(False)

    @mainthread
    def set_valid(self, value):
        self.valid = value
        if not value:
            toast("Invalid username")
            self.verified_username = []
        else:
            self.parent.parent.parent.parent.children[0].children[0].children[
                0
            ].disabled = False

    @mainthread
    def set_loading(self, value):
        self.loading = value


class ManualDialogMultipleContent(GridLayout):
    session = None
    """
    The backend session
    """

    valid = BooleanProperty(False)
    """
    Whether the username is valid
    """

    loading = BooleanProperty(False)
    """
    Whether the username is being validated
    """

    verified_username = []
    """
    The usernames that have been verified
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = Session()

    def enabled_validate(self, text):
        """
        Enables the validate button if there is text in the username field
        """
        self.ids.validate.disabled = text == ""
        # Reset the valid icon and the add button and the processed usernames
        if self.valid:
            self.valid = False
            self.parent.parent.parent.parent.children[0].children[0].children[
                0
            ].disabled = True
            self.verified_username = []

    def validate_username(self):
        """
        Validates the username
        """
        self.loading = True
        threading.Thread(target=self._validate_username).start()

    def _validate_username(self):
        """
        Validates the usernames on a separate thread
        """
        usernames = self.ids.usernames.text.split(",")
        valid = True
        wrong_usernames = []
        for username in usernames:
            try:
                Profile.from_username(self.session.loader.context, username.strip())
                self.verified_username.append(username.strip())
            except Exception:
                valid = False
                wrong_usernames.append(username)
        self.set_valid(valid, wrong_usernames)
        self.set_loading(False)

    @mainthread
    def set_valid(self, value, wrong_usernames):
        self.valid = value
        if not value:
            toast("Invalid username " + ", ".join(wrong_usernames) + " entered")
            self.verified_username = []
        else:
            self.parent.parent.parent.parent.children[0].children[0].children[
                0
            ].disabled = False

    @mainthread
    def set_loading(self, value):
        self.loading = value


class ManualDialogContent(GridLayout):
    individual_content: ManualDialogIndividualContent = None

    multiple_content: ManualDialogMultipleContent = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.individual_content = ManualDialogIndividualContent()
        self.multiple_content = ManualDialogMultipleContent()

    def change_content(self, *args):
        if self.ids.segmented_control.current_active_segment == self.ids.individual:
            self.ids.content.clear_widgets()
            self.individual_content.valid = False
            self.parent.parent.children[0].children[0].children[0].disabled = True
            self.ids.content.add_widget(self.individual_content)
        else:
            self.ids.content.clear_widgets()
            self.multiple_content.valid = False
            self.parent.parent.children[0].children[0].children[0].disabled = True
            self.ids.content.add_widget(self.multiple_content)


class ManualDialog(MDDialog):
    content_cls: ManualDialogContent = None

    ok_button: MDRaisedButton = None

    cancel_button: MDFlatButton = None

    def __init__(self, **kwargs):
        self.content_cls = ManualDialogContent()
        self.content_cls.individual_content.bind(on_valid=self.update_ok_button)
        self.content_cls.multiple_content.bind(on_valid=self.update_ok_button)
        self.ok_button = MDRaisedButton(text="Add Account")
        self.cancel_button = MDFlatButton(text="Cancel")
        self.cancel_button.bind(on_release=self.dismiss)
        super().__init__(
            title="Add Account",
            type="custom",
            content_cls=self.content_cls,
            buttons=[self.cancel_button, self.ok_button],
            **kwargs
        )

    def update_ok_button(self, *args):
        if (
            self.content_cls.ids.segmented_control.current_active_segment
            == self.content_cls.ids.individual
        ):
            self.ok_button.disabled = not self.content_cls.individual_content.valid
        else:
            self.ok_button.disabled = not self.content_cls.multiple_content.valid
