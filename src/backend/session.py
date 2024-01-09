from instaloader import Instaloader, Profile
from selenium import webdriver


class Session:
    """
    Maintains data about the current web sessions
    """

    _instance = None

    logged_in: bool = False
    loader: Instaloader = None
    driver: webdriver.Chrome = None
    username: str = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.loader = Instaloader()
        return cls._instance

    def login(self, username: str, password: str) -> Profile:
        """
        Login to Instagram using Instaloader
        """
        self.username = username
        self.loader.login(username, password)
        self.logged_in = True

    def clear(self):
        """
        Clears the current session
        """
        self.logged_in = False
        self.loader = Instaloader()
        self.driver = None
        self.username = None
