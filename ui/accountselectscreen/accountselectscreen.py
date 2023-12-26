import ast
import csv
import os
import subprocess
import sys
import threading

from instaloader import Hashtag, Profile
from kivy.clock import mainthread
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from plyer import filechooser

from backend.session import Session
from ui.components import (
    AddMenu,
    FollowerDialog,
    FollowingDialog,
    MainMenu,
    ManualDialog,
)
from ui.messagescreen import MessageScreen


class AccountSelectScreen(Screen):
    """
    Represents the data selection Screen.
    Allows the user to enter the accounts to message
    by manually entering them, from their followers
    or from a certain hashtag
    """

    addmenu = None
    """
    The add menu that is shown when the add button is pressed
    """

    mainmenu = None
    """
    The main menu that is shown when the menu button is pressed
    """

    session = None
    """
    The session object that is used to login to instagram
    """
    dialog = None
    data = []
    selected = []
    table = None
    content_cls = None

    csv_temp_data = []
    """
    The data that is used to store the csv data temporarily until verification
    """

    csv_failed_data = []
    """
    The data that is used to store the csv data that failed verification
    """

    def __init__(self, **kw):
        Builder.load_file("ui/accountselectscreen/accountselectscreen.kv")
        super().__init__(**kw)
        # add the MDDataTable to the layout
        self.ids.tablecontainer.add_widget(self.create_datatable(), 1)
        self.ids.tablecontainer.do_layout()
        self.session = Session()
        self.do_layout()

    def on_enter(self, *args):
        """
        Fired when the entering the screen. Is used to check if the message
        screen was added and if so it is deleted
        """
        if self.manager.has_screen("messagescreen"):
            self.manager.remove_widget(self.manager.get_screen("messagescreen"))

    def create_datatable(self):
        table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("S.No", dp(30)),
                ("Account Name", dp(80)),
                ("Account Source", dp(40)),
            ],
            check=True,
        )
        self.table = table
        self.table.bind(on_check_press=self.edit_selection)
        return table

    def edit_selection(self, *args):
        """Function that is called when there is any change
        to the selection of accounts
        """
        self.selection = self.table.get_row_checks()
        if len(self.selection) > 0:
            self.ids.next.disabled = False
            self.ids.Delete.disabled = False
        else:
            self.ids.next.disabled = True
            self.ids.Delete.disabled = True

    def verify_delete(self):
        """
        Verifies if the user wants to delete the selected accounts
        """
        ok_button = MDRaisedButton(text="Delete")
        cancel_button = MDFlatButton(text="Cancel")
        dialog = MDDialog(
            title="Delete Accounts",
            text="Are you sure you want to delete the selected accounts?",
            buttons=[cancel_button, ok_button],
        )
        ok_button.bind(on_release=self.delete_selected)
        cancel_button.bind(on_release=dialog.dismiss)
        dialog.open()

    def delete_selected(self, widget):
        """
        Removes the selected accounts from the list
        """
        widget.parent.parent.parent.parent.dismiss()
        for selected in self.selection:
            for stuff in self.data:
                if stuff[1] == selected[1]:
                    self.data.remove(stuff)
        self._update_table()

    def open_filepicker(self):
        """
        Opens the file picker to select a directory to export csv to
        """
        filechooser.save_file(on_selection=self.export_csv, filters=["*.csv"])

    def export_csv(self, path):
        """
        Exports the data to a csv file
        """
        self.mainmenu.dismiss()
        # convert the os path to a string
        if path[0] == "":
            toast("Enter a proper File Name")
            return
        path = path[0] if path[0].endswith(".csv") else path[0] + ".csv"
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Account Name", "Account Source"])
            writer.writerows(self.data)
        toast("Exported to CSV")

    def import_csv(self):
        """
        Imports the data from a csv file
        """
        filechooser.open_file(on_selection=self._import_csv_file)

    def _import_csv_file(self, path):
        """
        Imports the data from a csv file
        """
        self.addmenu.dismiss()
        for file in path:
            with open(file, newline="") as file:
                reader = csv.reader(file)
                header = next(reader)  # Get the first row (header)
                if header[0] != "Account Name":
                    toast("Invalid CSV File. Check ")
                    return
                else:
                    for row in reader:
                        if len(self.data):
                            number = self.data[-1][0] + 1
                        else:
                            if len(self.csv_temp_data):
                                number = self.csv_temp_data[-1][0] + 1
                            else:
                                number = 1
                        temp = (number, row[1], ast.literal_eval(row[2]))
                        self.csv_temp_data.append(temp)
        # Ask user if they want to validate the accounts in a dialog
        ok_button = MDRaisedButton(text="Verify")
        cancel_button = MDFlatButton(text="Don't Verify")
        dialog = MDDialog(
            title="Validate Accounts",
            text="Do you want to Verify the accounts Exists? This will take more time",
            buttons=[cancel_button, ok_button],
        )
        ok_button.bind(on_release=self.verify_accounts)
        cancel_button.bind(on_release=self.dont_verify_accounts)
        dialog.open()

    def verify_accounts(self, widget):
        """
        Validates the accounts in the list
        """
        widget.parent.parent.parent.parent.dismiss()
        event = threading.Event()
        thread = threading.Thread(target=self._verify_accounts, args=(event,))
        thread.name = "CSV Import"
        task = {
            "name": "Verify CSV Accounts",
            "thread": thread,
            "progress": 0,
            "max": len(self.csv_temp_data),
            "event": event,
        }
        if (self.ids.progress.check_if_can_add_task(task["name"])) is False:
            toast("Task already running")
            return
        self.ids.progress.add_task(task)
        thread.start()

    def _verify_accounts(self, event):
        """
        Verifies the accounts in the list
        """
        count = 0
        for account in self.csv_temp_data:
            if event.is_set():
                self.ids.progress.update_task(
                    "Verify CSV Accounts",
                    len(self.csv_temp_data),
                    len(self.csv_temp_data),
                )
                return
            try:
                Profile.from_username(self.session.loader.context, account[1])
            except Exception:
                self.csv_failed_data.append(account)
                self.csv_temp_data.remove(account)
            count += 1
            self.ids.progress.update_task(
                "Verify CSV Accounts", count, len(self.csv_temp_data)
            )
        self.data.extend(self.csv_temp_data)
        self._update_table()
        if (len(self.csv_failed_data)) > 0:
            toast("Some accounts failed to verify. They where not added to the list")
        self.csv_temp_data = []
        self.csv_failed_data = []

    def dont_verify_accounts(self, widget):
        """
        Adds the accounts from the csv file without verifying
        """
        widget.parent.parent.parent.parent.dismiss()
        self.data.extend(self.csv_temp_data)
        self._update_table()
        self.csv_temp_data = []

    def show_hashtag_dialog(self):
        """
        Shows the hashtag dialog
        """
        pass

        #     ok_button = MDFlatButton(text="OK")
        #     cancel_button = MDFlatButton(text="CANCEL")
        #     self.content_cls = HashtagDialog()
        #     self.dialog = MDDialog(
        #         title="Enter the Hashtags",
        #         type="custom",
        #         content_cls=self.content_cls,
        #         buttons=[
        #             ok_button,
        #             cancel_button,
        #         ],
        #     )
        #     ok_button.bind(on_release=self.get_hashtag_accounts)
        #     cancel_button.bind(on_release=self.dialog.dismiss)
        #     self.dialog.open()

        # def get_hashtag_accounts(self, widget):
        #     threading.Thread(
        #         target=self._get_hashtag_accounts,
        #         args=(
        #             self.content_cls.ids.hashtags.text,
        #             int(self.content_cls.ids.limit.text),
        #         ),
        #     ).start()
        #     self.dialog.dismiss()

    def show_follower_popup(self):
        """
        Shows the follower popup
        """
        self.addmenu.dismiss()
        popup = FollowerDialog(self.session.loader.context, self.session.username)
        popup.ok_button.bind(on_release=self.get_follow_accounts)
        popup.open()

    def get_follow_accounts(self, widget):
        widget.parent.parent.parent.parent.dismiss()
        limit = widget.parent.parent.parent.parent.selected_followers
        event = threading.Event()
        thread = threading.Thread(target=self._get_follow_accounts, args=(event, limit))
        thread.name = "Followers"
        task = {
            "name": "Followers",
            "thread": thread,
            "progress": 0,
            "max": limit,
            "event": event,
        }
        if (self.ids.progress.check_if_can_add_task(task["name"])) is False:
            toast("Task already running")
            return
        self.ids.progress.add_task(task)
        thread.start()

    def _get_follow_accounts(self, event, limit):
        """
        gets the accounts from the followers of the account
        """
        profile = Profile.from_username(
            self.session.loader.context, self.session.username
        )
        followers = profile.get_followers()
        count = 0
        for follower in followers:
            if event.is_set():
                self.ids.progress.update_task("Followers", limit, limit)
                return
            if count == limit:
                break
            if len(self.data):
                number = self.data[-1][0] + 1
            else:
                number = 1
            temp = (number, follower.username, ("instagram", "Followers"))
            self.data.append(temp)
            count += 1
            self.ids.progress.update_task("Followers", count, limit)
        self._update_table()

    def show_following_dialog(self):
        """
        Shows the following dialog
        """
        self.addmenu.dismiss()
        popup = FollowingDialog(self.session.loader.context, self.session.username)
        popup.ok_button.bind(on_release=self.get_following_accounts)
        popup.open()

    def get_following_accounts(self, widget):
        widget.parent.parent.parent.parent.dismiss()
        limit = widget.parent.parent.parent.parent.selected_following
        event = threading.Event()
        thread = threading.Thread(
            target=self._get_following_accounts, args=(event, limit)
        )
        thread.name = "Following"
        task = {
            "name": "Followees",
            "thread": thread,
            "progress": 0,
            "max": limit,
            "event": event,
        }
        if (self.ids.progress.check_if_can_add_task(task["name"])) is False:
            toast("Task already running")
            return
        self.ids.progress.add_task(task)
        thread.start()

    def _get_following_accounts(self, event, limit):
        """
        gets the accounts from the following of the account
        """
        profile = Profile.from_username(
            self.session.loader.context, self.session.username
        )
        followees = profile.get_followees()
        count = 0
        for followee in followees:
            if event.is_set():
                self.ids.progress.update_task("Followees", profile.followers, limit)
                return
            if count == limit:
                break
            if len(self.data):
                number = self.data[-1][0] + 1
            else:
                number = 1
            temp = (
                number,
                followee.username,
                ("chart-timeline-variant-shimmer", "Followees"),
            )
            self.data.append(temp)
            count += 1
            self.ids.progress.update_task("Followees", count, limit)
        self._update_table()

    def show_manual_dialog(self):
        """
        Shows the Manual entry of accounts
        """
        self.addmenu.dismiss()
        popup = ManualDialog()
        popup.ok_button.disabled = True
        popup.ok_button.bind(on_release=self.add_manual_accounts)
        popup.open()

    def add_manual_accounts(self, widget):
        """
        Adds the accounts from the manual dialog
        """
        widget.parent.parent.parent.parent.dismiss()
        popup = widget.parent.parent.parent.parent
        accounts = (
            popup.content_cls.individual_content.verified_username
            + popup.content_cls.multiple_content.verified_username
        )
        for account in accounts:
            if len(self.data):
                number = self.data[-1][0] + 1
            else:
                number = 1
            temp = (number, account, ("account", "Manual"))
            self.data.append(temp)
        self._update_table()

    def _get_hashtag_accounts(self, hashtags_string: str, limit: int):
        """
        gets the first certain number of accounts from each hashtag
        """
        # extract the hashtags from the string
        hashtags = hashtags_string.split(",")
        for hashtag in hashtags:
            hg = Hashtag.from_name(self.session.loader.context, hashtag)
            posts = hg.get_posts_resumable()
            count = 0
            for post in posts:
                if count == limit:
                    break
                if len(self.data):
                    number = self.data[-1][0] + 1
                else:
                    number = 1
                temp = (number, post.owner_username, "Hashtag")
                self.data.append(temp)
                count += 1
        self._update_table()

    @mainthread
    def _update_table(self):
        """
        Updates the table with the data
        """
        # recalculate the sno column
        for index, row in enumerate(self.data):
            self.data[index] = (index + 1, row[1], row[2])
        self.table.update_row_data(self.table, self.data)
        self.edit_selection()

    def show_mainmenu(self):
        """
        Shows the menu
        """
        self.mainmenu = MainMenu(
            export=self.open_filepicker,
            settings=self.show_settings_dialog,
            launch_instance=self.launch_instance,
            about=self.show_about_dialog,
            switch_user=self.switch_user,
            caller=self.ids.menu,
        )
        self.mainmenu.open()

    def show_add_menu(self):
        """
        Shows the add menu
        """
        self.addmenu = AddMenu(
            followers=self.show_follower_popup,
            following=self.show_following_dialog,
            hashtag=self.show_hashtag_dialog,
            manual=self.show_manual_dialog,
            importfile=self.import_csv,
            caller=self.ids.addbutton,
        )
        self.addmenu.open()

    def navigate_to_message(self):
        """
        Navigates to the message screen
        """
        self.manager.add_widget(MessageScreen(name="messagescreen", data=self.data))
        self.manager.current = "messagescreen"

    def show_settings_dialog(self):
        """
        Shows the settings dialog
        """
        pass

    def launch_instance(self):
        """
        Launches a new instance of the program
        """
        subprocess.Popen(
            [
                sys.executable,
                os.path.join(os.path.dirname(sys.executable), "..\\..\\main.py"),
            ]
        )

    def show_about_dialog(self):
        """
        Shows the about dialog
        """
        pass

    def switch_user(self):
        """
        Takes the user back to the user selection screen, clears the current screen and session
        """
        self.mainmenu.dismiss()
        self.session.clear()
        from ui.welcomescreen.welcomescreen import WelcomeScreen

        # remove the message screen if it exists
        if self.manager.has_screen("messagescreen"):
            self.manager.remove_widget(self.manager.get_screen("messagescreen"))
        self.manager.switch_to(WelcomeScreen(name="welcome"), direction="right")
