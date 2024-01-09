from kivymd.uix.menu import MDDropdownMenu


class AddMenu(MDDropdownMenu):
    def __init__(self, followers, following, hashtag, manual, importfile, **kwargs):
        self.pos = (400, 400)
        super().__init__(**kwargs)
        self.items = [
            {
                "text": "From Followers",
                "leading_icon": "instagram",
                "on_release": followers,
            },
            {
                "text": "From Following",
                "leading_icon": "chart-timeline-variant-shimmer",
                "on_release": following,
            },
            {
                "text": "From A Hashtag (Coming Soon)",
                "leading_icon": "pound",
                "on_release": hashtag,
            },
            {"text": "Manual Entry", "leading_icon": "account", "on_release": manual},
            {
                "text": "Import From CSV",
                "leading_icon": "file-import",
                "on_release": importfile,
            },
        ]
