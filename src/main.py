from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from backend import DatabaseManager, Session
from ui.welcomescreen import WelcomeScreen
import sys
import os


# Define the path for the icon
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # Running as a bundled executable (PyInstaller)
    ICON = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "ui/assets/icon.png")
    )

else:
    # Inside a normal Python environment"
    ICON = "ui/assets/icon.png"


class MyApp(MDApp):
    """The main App Class"""

    backend_sess: Session = Session()
    """
    Backend Session
    """

    title: str = "MR.DM"
    """
    Title of the application
    """

    icon: str = ICON
    """
    Path to the icon of the application
    """

    def build(self) -> ScreenManager:
        """The build method of the application

        :return: ScreenManager of the application
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
        # dismiss the splash screen
        try:
            import pyi_splash

            pyi_splash.close()
        except Exception:
            pass
        return sm


if __name__ == "__main__":
    MyApp().run()
