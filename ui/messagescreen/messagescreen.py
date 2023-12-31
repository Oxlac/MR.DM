import os
import sys
from time import sleep
from typing import Any

from kivy.clock import mainthread
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ui.components import MessageMenu
from ui.components.message_components import LinkMessage, PostMessage, TextMessage
from ui.progressscreen import ProgressScreen


class MessageScreen(Screen):
    data: Any = None
    message: str = None
    reel_link: str = None
    session: webdriver.Chrome = None
    processed_accounts = []

    add_message_menu = None
    """
    Stores an instance of the add message menu
    """

    data = []
    """
    Stores the Target Account data sent from the account select screen
    """

    messages = []
    """
    Stores the messages to be sent. Each message is a dictionary representing the
    message type and the message content
    """

    def __init__(self, data, *args: Any, **kwds: Any) -> Any:
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            # Running as a bundled executable (PyInstaller)
            Builder.load_file(
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "messagescreen.kv")
                )
            )
        else:
            # Inside a normal Python environment
            Builder.load_file("ui/messagescreen/messagescreen.kv")
        self.data = data
        return super().__init__(*args, **kwds)

    def show_add_message_menu(self):
        """
        Shows the add message menu
        """
        self.add_message_menu = MessageMenu(
            text=self.add_text_message,
            link=self.add_link_message,
            post=self.add_post_message,
            caller=self.ids.add_message,
        )
        self.add_message_menu.open()

    def add_text_message(self):
        """
        Adds a text message to the message box
        """
        self.add_message_menu.dismiss()
        self.ids.message_container.add_widget(TextMessage())

    def add_link_message(self):
        """
        Adds a link message to the message box
        """
        self.add_message_menu.dismiss()
        self.ids.message_container.add_widget(LinkMessage())

    def add_post_message(self):
        """
        Adds a post message to the message box
        """
        self.add_message_menu.dismiss()
        self.ids.message_container.add_widget(PostMessage())

    def check_if_can_add(self):
        """
        Checks if we are under the maximum number of messages
        """
        if len(self.ids.message_container.children) < 4:
            self.show_add_message_menu()
        else:
            toast("You can only add 4 messages at a time")

    def back(self):
        """
        Goes back to the account select screen
        """
        self.manager.current = "accountselect"

    def confirm_send(self):
        """
        Confirms that the user wants to send the messages
        """
        self.confirm_send_dialogue = None
        ok_button = MDFlatButton(text="OK", on_release=self.navigate_to_progress)
        cancel_button = MDFlatButton(
            text="Cancel", on_release=lambda x: self.confirm_send_dialogue.dismiss()
        )
        self.confirm_send_dialogue = MDDialog(
            title="Confirm",
            text="Are you sure you want to send these messages to "
            + str(len(self.data))
            + " users?",
            buttons=[ok_button, cancel_button],
        )
        self.confirm_send_dialogue.open()

    @mainthread
    def navigate_to_progress(self, *args):
        """
        Navigates to the progress screen
        """
        self.confirm_send_dialogue.dismiss()
        for message in self.ids.message_container.children:
            if message.ids.content.text == "":
                toast("Please fill in all fields")
                return
            self.messages.append(
                {
                    "type": message.__class__.__name__,
                    "content": message.ids.content.text,
                }
            )
        self.manager.add_widget(
            ProgressScreen(name="progress", messages=self.messages, accounts=self.data)
        )
        self.manager.current = "progress"
        self.manager.remove_widget(self)
