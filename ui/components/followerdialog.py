import threading

from instaloader import Profile
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

Builder.load_string(
    """
<FollowerPopupContent>:
    orientation: "vertical"
    padding: dp(5)
    size_hint_y: None
    height: dp(150)

    MDTextField:
        id: follower_count
        hint_text: "Amount of Followers to Load"
        helper_text: "Use [1-n]% for relative. Leave empty for all"
        helper_text_mode: "persistent"
        mode: "rectangle"
        pos_hint: {"center_x": .5, "center_y": .5}
        on_text: root.parent.parent.parent.update_text(self.text)
    MDLabel:
        id: follower_count_label
        text: "100 followers will be loaded"

<FollowerDialog>:

    """
)


class FollowerPopupContent(BoxLayout):
    pass


class FollowerDialog(MDDialog):
    content_cls: FollowerPopupContent = None

    ok_button: MDRaisedButton = None

    cancel_button: MDFlatButton = None

    total_followers = NumericProperty(0)

    selected_followers = NumericProperty(0)

    loading = BooleanProperty(False)

    def __init__(self, session, username, **kwargs):
        self.content_cls = FollowerPopupContent()
        self.ok_button = MDRaisedButton(text="Load Followers")
        self.cancel_button = MDFlatButton(text="Cancel")
        self.cancel_button.bind(on_release=self.dismiss)
        self.session = session
        self.username = username
        super().__init__(
            title="Select Follower Count",
            type="custom",
            text="Enter the follower count",
            content_cls=FollowerPopupContent(),
            buttons=[self.cancel_button, self.ok_button],
        )
        threading.Thread(target=self.load_total_followers).start()

    def load_total_followers(self):
        """
        Runs on a background thread and loads the total number of followers
        this account has
        """
        self.loading = True
        self.ok_button.disabled = True
        self.content_cls.ids.follower_count_label.text = "Loading..."
        self.content_cls.ids.follower_count.disabled = True
        profile = Profile.from_username(self.session, self.username)
        self.total_followers = profile.followers
        self.loading = False
        self.ok_button.disabled = False
        self.update_text("")
        self.content_cls.ids.follower_count.disabled = False

    def update_text(self, text, *args):
        """
        Updates the text of the label
        """
        if text == "":
            self.selected_followers = self.total_followers
            self.content_cls.ids.follower_count_label.text = (
                f"{self.selected_followers} followers will be loaded"
            )
            return
        if "%" in text:
            self.selected_followers = int(self.total_followers * (int(text[:-1]) / 100))
        else:
            self.selected_followers = int(text)
        # check if the selected followers is greater than the total followers
        if self.selected_followers > self.total_followers:
            self.selected_followers = self.total_followers

        self.content_cls.ids.follower_count_label.text = (
            f"{self.selected_followers} followers will be loaded"
        )
