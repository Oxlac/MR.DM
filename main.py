from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp


from backend import DatabaseManager, Session
from ui.welcomescreen import WelcomeScreen


class MyApp(MDApp):
    """The main App Class

    :param MDApp: KivyMD App Class
    :type MDApp: class `MDApp` from `kivymd.app` module
    """    
    backend_sess = Session()
    """
    Backend Session
    """

    title = "MR.DM"
    """
    Title of the application
    """

    icon = "ui/assets/icon.png"
    """
    Icon of the application
    """

    def build(self):
        """The build method of the application

        :return: ScreenManager of the application
        :rtype: `ScreenManager` from `kivy.uix.screenmanager` module
        """
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M3"
        sm = ScreenManager()
        # sm.switch_to(MessageScreen(name="message", data=[]), direction="left")
        sm.switch_to(WelcomeScreen(name="welcome"), direction="left")
        # Create Database
        inspector.create_inspector(Window, sm)
        DatabaseManager().create_tables()
        return sm


if __name__ == "__main__":
    MyApp().run()
