import threading

from instaloader import Profile
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

Builder.load_string(
    """
<FollowingDialogContent>:
    orientation: "vertical"
    padding: dp(5)
    size_hint_y: None
    height: dp(150)

    MDTextField:
        id: following_count
        hint_text: "Amount of Followees to Load"
        helper_text: "Use [1-n]% for relative. Leave empty for all"
        helper_text_mode: "persistent"
        mode: "rectangle"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_text: root.parent.parent.parent.update_text(self.text)
    MDLabel:
        id: following_count_label
        text: "100 followers will be loaded"

<FollowingDialog>:

    """
)


class FollowingDialogContent(BoxLayout):
    pass


class FollowingDialog(MDDialog):
    content_cls: FollowingDialogContent = None

    ok_button: MDRaisedButton = None

    cancel_button: MDFlatButton = None

    total_following = NumericProperty(0)

    selected_following = NumericProperty(0)

    loading = BooleanProperty(False)

    def __init__(self, session, username, **kwargs):
        self.ok_button = MDRaisedButton(text="Load Followees")
        self.cancel_button = MDFlatButton(text="Cancel")
        self.cancel_button.bind(on_release=self.dismiss)
        self.session = session
        self.username = username
        super().__init__(
            title="Select Followee Count",
            type="custom",
            content_cls=FollowingDialogContent(),
            buttons=[self.cancel_button, self.ok_button],
        )
        threading.Thread(target=self.load_total_followee).start()

    def load_total_followee(self):
        """
        Runs on a background thread and loads the total number of followers
        this account has
        """
        self.loading = True
        self.ok_button.disabled = True
        self.content_cls.ids.following_count_label.text = "Loading..."
        self.content_cls.ids.following_count.disabled = True
        profile = Profile.from_username(self.session, self.username)
        self.total_following = profile.followees
        self.loading = False
        self.ok_button.disabled = False
        self.update_text("")
        self.content_cls.ids.following_count.disabled = False

    def update_text(self, text, *args):
        """
        Updates the text of the label
        """
        if text == "":
            self.selected_following = self.total_following
            self.content_cls.ids.following_count_label.text = (
                f"{self.selected_following} followers will be loaded"
            )
            return
        if "%" in text:
            self.selected_following = int(self.total_following * (int(text[:-1]) / 100))
        else:
            self.selected_following = int(text)
        # check if the selected followers is greater than the total followers
        if self.selected_following > self.total_following:
            self.selected_following = self.total_following

        self.content_cls.ids.following_count_label.text = (
            f"{self.selected_following} followers will be loaded"
        )
