from ast import Dict

from kivy.animation import Animation
from kivy.clock import mainthread
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon

Builder.load_string(
    """
<AccountProgress>:
    canvas.before:
        Color:
            rgba : self.theme_cls.primary_color if self.loading else (0,0,0,0)
        Ellipse:
            size: self.size[0] + dp(6) , self.size[1] + dp(6)
            pos: self.pos[0] - dp(3), self.pos[1] - dp(3)
            angle_start: 0
            angle_end: root.overall_progress

        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Ellipse:
            pos: self.pos
            size: self.size

    size_hint: None, None
    size: dp(42), dp(42)

    CustomIcon:
        id: icon
        size_hint:1,1
        pos_hint: {"center_x": 0.5, "center_y": 0.5}



<CustomIcon>:
    icon: "sync"
    theme_text_color: "Custom"
    text_color: self.theme_cls.primary_color

    
<ProgressPopup>:
    size_hint: None,None
    size: dp(260), dp(160)
    orientation: "vertical"
    padding: dp(15)
    spacing: dp(10)

    ScrollView:
        size_hint:1,.8
        do_scroll_x: False
        scroll_bar_width: dp(5)
        GridLayout:
            id:task_container
            cols: 1
            spacing: dp(15)
            size_hint:1,None

    RelativeLayout:
        size_hint:1,.15
        MDRectangleFlatButton:
            text: "Cancel All"
            pos_hint: {"right": 1, "center_y": 0.5}
            on_release: root.parent_container.cancel_all_tasks()

        MDFlatButton:
            text: "Clear Finished"
            pos_hint: {"left": 1, "center_y": 0.5}
            on_release: root.parent_container.clear_finished_tasks()




<ProgressItem>:
    size_hint: 1, None
    height: dp(40)
    padding: dp(10)

    BoxLayout:
        size_hint: 0.8, 1
        pos_hint: {"center_y": 0.5, "left": 1}
        orientation: "vertical"

        MDLabel:
            id: task_name
            text: root.task_name
            font_size: "14sp"
            bold: True

        MDLabel:
            id: task_status
            text: f"{root.task_progress}/{root.task_max}"
            font_size: "12sp"

    RelativeLayout:
        size_hint:None,None
        size: dp(30), dp(30)
        pos_hint: {"center_y": 0.5, "right": 0.95}
        MDIconButton:
            icon: "close"
            theme_text_color: "Secondary"
            pos_hint: {"center_y": 0.5, "center_x": 0.5}
            on_release: root.cancel_task()
            opacity: 1 if root.task_progress < root.task_max else 0
            disabled: True if root.task_progress > root.task_max else False
            icon_size: dp(20)

        MDSpinner:
            size_hint: None, None
            size: dp(30), dp(30)
            pos_hint: {"center_y": 0.5, "center_y": 0.5}
            active: True if root.task_progress < root.task_max else False

        MDIcon:
            id: icon
            icon: "check"
            theme_text_color: "Custom"
            text_color: 0, 1, 0, 1
            size_hint: None, None
            size: dp(20), dp(20)
            pos_hint: {"center_y": 0.5, "center_x": 0.5}
            opacity: 1 if root.task_progress >= root.task_max else 0

    """
)


class CustomIcon(MDIcon, RotateBehavior):
    pass


class ProgressPopup(MDCard):
    parent_container = ObjectProperty()
    """
    Stores the popup object
    """

    def __init__(self, *args, parent_container, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_container = parent_container


class ProgressItem(RelativeLayout):
    task_name = StringProperty()

    task_thread = ObjectProperty()

    task_progress = NumericProperty()

    task_max = NumericProperty()

    event = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

    def cancel_task(self):
        """
        Cancels the task
        """
        self.event.set()
        toast(self.task_name + " cancelled")
        # set the task to finished and set a custom icon to show it was cancelled
        self.task_progress = self.task_max
        self.ids.icon.icon = "alert-circle"
        self.ids.icon.theme_text_color = "Error"
        self.ids.task_status.text = "Cancelled"


class AccountProgress(ButtonBehavior, FloatLayout, ThemableBehavior):
    loading = BooleanProperty(False)

    tasks = ListProperty([])
    """
    List of tasks to be completed. Stores the task name and
    its current state. Acts as the reference for all tasks
    """

    popup = None
    """
    Stores the popup object
    """

    popup_shown = BooleanProperty(False)
    """
    Stores whether the popup is shown or not
    """

    overall_progress = NumericProperty(0)

    def __init__(self, **kw):
        self.popup = ProgressPopup(parent_container=self)
        # dummy_task = {
        #     "name": "Follower",
        #     "thread": None,
        #     "progress": 10,
        #     "max": 10,
        # }
        # self.add_task(dummy_task)
        # dummy_second_task = {
        #     "name": "Following",
        #     "thread": None,
        #     "progress": 5,
        #     "max": 10,
        # }
        # self.add_task(dummy_second_task)
        super().__init__(**kw)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) is False:
            if self.popup_shown:
                self.close_menu()
        return super().on_touch_down(touch)

    def on_loading(self, *args):
        """
        Called when the loading property is changed
        """
        if self.loading:
            # animate the center icon to rotate continuously
            icon = self.ids.icon
            self.anim = Animation(rotate_value_angle=360, duration=1, t="in_out_circ")
            self.anim += Animation(rotate_value_angle=0, duration=0)
            self.anim.repeat = True
            self.anim.start(icon)
        else:
            # stop the animation
            icon = self.ids.icon
            icon.angle = 0
            self.anim.cancel(icon)

    def check_if_can_add_task(self, task_name: str):
        """
        Checks if a task can be added to the list of tasks
        """
        for task in self.tasks:
            if task["name"] == task_name:
                if task["progress"] != task["max"]:
                    return False
        return True

    def add_task(self, task: Dict):
        """
        Adds a task to the list of tasks
        """
        # clear all the finished tasks
        self.clear_finished_tasks()
        # creates a new progress item and adds it to the popup
        item = ProgressItem()
        item.task_name = task["name"]
        item.task_thread = task["thread"]
        item.task_progress = task["progress"]
        item.task_max = task["max"]
        item.event = task["event"]
        self.popup.ids.task_container.add_widget(item)
        updated_task = {
            "name": task["name"],
            "thread": task["thread"],
            "progress": task["progress"],
            "max": task["max"],
            "item": item,
            "event": task["event"],
        }
        self.tasks.append(updated_task)

    @mainthread
    def get_task(self, name: str):
        """
        Gets a task from the list of tasks
        """
        for task in self.tasks:
            if task["name"] == name:
                return task

    @mainthread
    def update_task(self, name: str, progress: int, max: int):
        """
        Updates a task progress in the list of tasks
        """
        for task in self.tasks:
            if task["name"] == name:
                task["progress"] = progress
                task["max"] = max
                task["item"].task_progress = progress
                task["item"].task_max = max
                self.on_tasks()

    @mainthread
    def on_tasks(self, *args):
        """
        Used to update the summary progress UI
        """
        total_tasks = len(self.tasks)
        finished_tasks = 0
        for task in self.tasks:
            if task["progress"] == task["max"]:
                finished_tasks += 1
        if finished_tasks == total_tasks:
            self.loading = False
        else:
            self.loading = True
        # calculate overall progress
        if len(self.tasks) > 0:
            op = 0
            om = 0
            for task in self.tasks:
                op += task["progress"]
                om += task["max"]
            # convert to degrees
            self.overall_progress = (op / om) * 360

    def on_release(self):
        """
        Opens menu to show progress of tasks
        """
        self.open_menu()
        return super().on_release()

    def open_menu(self):
        if not self.popup_shown:
            # Allows the popup to open under the button
            window_cords = self.to_window(*self.pos)
            self.parent.parent.parent.add_widget(self.popup)
            self.popup.pos = (
                window_cords[0] - self.popup.size[0] + dp(42),
                window_cords[1] - self.popup.size[1] - dp(10),
            )
            self.popup_shown = True
        else:
            self.close_menu()

    def close_menu(self):
        """
        Closes the menu
        """
        self.popup_shown = False
        self.parent.parent.parent.remove_widget(self.popup)

    def clear_finished_tasks(self):
        """
        Clears all the finished tasks
        """
        for task in self.tasks:
            if task["progress"] == task["max"]:
                self.tasks.remove(task)
                self.popup.ids.task_container.remove_widget(task["item"])

    def cancel_all_tasks(self):
        """
        Cancels all the tasks
        """
        for task in self.tasks:
            task["event"].set()
            task["item"].cancel_task()
            self.tasks.remove(task)
            self.popup.ids.task_container.remove_widget(task["item"])
        self.close_menu()
