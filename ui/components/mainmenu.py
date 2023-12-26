from kivymd.uix.menu import MDDropdownMenu


class MainMenu(MDDropdownMenu):
    def __init__(self, export, settings, launch_instance, about, switch_user, **kwargs):
        self.pos = (400, 400)
        super().__init__(**kwargs)
        self.items = [
            {
                "text": "Export to CSV",
                "leading_icon": "file-export",
                "on_release": export,
            },
            {
                "text": "Settings",
                "leading_icon": "cog",
                "on_release": settings,
            },
            {
                "text": "Start New Instance",
                "leading_icon": "rocket-launch",
                "on_release": launch_instance,
            },
            {
                "text": "About This Program",
                "leading_icon": "information",
                "on_release": about,
            },
            {
                "text": "Switch User",
                "leading_icon": "account-switch",
                "on_release": switch_user,
            },
        ]
