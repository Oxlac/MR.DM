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
            ProgressScreen(
                name="progress_screen", messages=self.messages, accounts=self.data
            )
        )
        self.manager.current = "progress_screen"

    def message_loop(self):
        """
        This is the main function that deals with sending messages
        to each user in the list
        """
        for user in self.data:
            # compose a new message for the user
            self.find_element(
                "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div"
            ).click()
            sleep(3)
            actions = webdriver.ActionChains(self.session.driver)
            actions.send_keys(user[1])
            actions.perform()
            sleep(2)
            actions = webdriver.ActionChains(self.session.driver)
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            sleep(2)
            actions = webdriver.ActionChains(self.session.driver)
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            sleep(3)
            # start typing the message
            actions = webdriver.ActionChains(self.session.driver)
            actions.send_keys(self.reel_link)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            sleep(2)
            # send the message
            actions = webdriver.ActionChains(self.session.driver)
            actions.send_keys(self.message)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            sleep(10)
            # add the user to the processed list
            self.processed_accounts.append(user[0])
            # update the progress bar
            self.update_progress()

        # finish the process
        self.finish()

    @mainthread
    def update_progress(self):
        self.ids.progress.value = len(self.processed_accounts)
        self.ids.progress_label.text = (
            str(len(self.processed_accounts)) + "/" + str(len(self.data))
        )

    def finish(self):
        self.ids.progress_label.text = "Finished"
        self.ids.progress.label.bg_color = (0, 1, 0, 1)
        # save the processed accounts to a file
        with open("processed_accounts.txt", "w") as f:
            for account in self.processed_accounts:
                f.write(account + "\n")
