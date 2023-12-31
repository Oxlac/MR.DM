import json
import os
import sys
from functools import partial
from threading import Thread

from instaloader import BadCredentialsException, Profile, TwoFactorAuthRequiredException
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from backend.database import DatabaseManager
from backend.session import Session
from ui.accountselectscreen import AccountSelectScreen
from ui.components import NewAccountPopup, UserCard


class WelcomeScreen(Screen):
    """
    Class for the welcome screen
    """

    session = None

    processing: BooleanProperty = BooleanProperty(False)

    def __init__(self, **kw):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            # Running as a bundled executable (PyInstaller)
            Builder.load_file(
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "welcomescreen.kv")
                )
            )
        else:
            # Inside a normal Python environment
            Builder.load_file("ui/welcomescreen/welcomescreen.kv")
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        """
        Called before the screen is entered
        """
        self.load_accounts()

    def load_accounts(self):
        """
        Loads accounts from database and displays them on the welcome screen
        """
        # clear the container
        self.ids.users_container.clear_widgets()
        users = DatabaseManager().get_users()
        if len(users) != 0:
            self.ids.users_container.clear_widgets()
        for user in users:
            card = UserCard(
                username=user[1],
                profile_pic_url=user[2],
                userid=user[0],
                delete_callback=self.confirm_logout,
            )
            card.bind(on_release=self.set_new_session)
            self.ids.users_container.add_widget(card)

    def add_account(self):
        """
        Adds an account to the database
        """
        popup = NewAccountPopup()
        popup.ok_button.bind(on_release=partial(self.login_user, popup))
        popup.open()

    def login_user(self, popup, *args):
        """
        Logs in a user
        """
        popup.dismiss()
        username = popup.content_cls.ids.username.text
        password = popup.content_cls.ids.password.text
        if username == "" or password == "":
            toast("Please fill in all fields")
            return
        self.processing = True
        Thread(target=self._login_user, args=(username, password)).start()

    def _login_user(self, username, password):
        """
        Runs on a separate thread to login a user
        """
        try:
            self.session = Session()
            self.session.login(username, password)
            profile = Profile.from_username(
                self.session.loader.context, self.session.username
            )
            self.save_to_database(profile)
        except BadCredentialsException:
            self.toast_Error("Invalid username or password")
            return

        except TwoFactorAuthRequiredException:
            self.toast_Error("Two factor authentication is not supported")
            return

        except Exception as e:
            self.toast_Error(e)
            return

    def confirm_logout(self, widget):
        """
        Confirms the logout of a user
        """
        # Show confirmation Dialog
        self.dialog = MDDialog(
            title="Logout of " + widget.username + "?",
            text="This will remove the account from the database and you will have to re-enter your login details to access your account. You can also logout from the settings screen.",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                ),
                MDRaisedButton(
                    text="Logout",
                    on_release=partial(self.logout_user, widget),
                ),
            ],
        )
        self.dialog.open()

    def logout_user(self, user, widget):
        """
        Logs Out an user
        """
        DatabaseManager().delete_user(user.userid)
        self.load_accounts()
        self.dialog.dismiss()

    @mainthread
    def toast_Error(self, e):
        toast(str(e), duration=10)
        self.processing = False
        return

    @mainthread
    def save_to_database(self, profile):
        """Saves the new user to the database

        :param profile: profile of the user
        :type profile: Profile
        """
        DatabaseManager().add_user(
            profile.userid,
            profile.username,
            profile.profile_pic_url,
            json.dumps(self.session.loader.save_session()),
        )
        self.processing = False
        self.navigate_to_next_screen()

    def set_new_session(self, widget):
        """
        loads the sesion of the user into the backend
        """
        user = DatabaseManager().get_user(widget.userid)
        session_data = json.loads(user[3])
        self.session = Session()
        self.session.loader.load_session(username=user[1], session_data=session_data)
        self.session.username = user[1]
        self.navigate_to_next_screen()

    def navigate_to_next_screen(self, widget=None):
        """
        Navigates to the next screen
        """
        self.manager.switch_to(
            AccountSelectScreen(name="accountselect"), direction="left"
        )
