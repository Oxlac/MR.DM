import sqlite3
from typing import List, Tuple


class DatabaseManager:
    """
    Creates and manages a database connection to the SQLite database. This class is a singleton class.
    """

    _instance = None
    """
    The singleton instance of the class
    """

    conn: sqlite3.Connection = None
    """
    Sqlite connection object
    """

    def __new__(cls) -> "DatabaseManager":
        """
        This class is a singleton class. This method ensures that only one instance of this class is created.

        :return: Returns the singleton instance of the class
        """
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect("data.db")
            cls._instance.create_tables()
        return cls._instance

    def create_tables(self) -> None:
        """
        Called at the start of the application to create the required tables in the database.
        """
        c = self.conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userid INTEGER PRIMARY KEY,
                username TEXT,
                profile_pic_url TEXT,
                session BLOB
            )
            """
        )
        self.conn.commit()

    def get_user(self, userid: str) -> Tuple[str, str, str, str]:
        """
        Gets the Instagram user from the database with the given userid.

        :param userid: The userid of the user to get

        :return: The user with the given userid
        """

        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE userid=?", (userid,))
        return c.fetchone()

    def add_user(
        self, userid: str, username: str, profile_pic_url: str, session: str
    ) -> None:
        """
        Adds a new Instagram user to the database.

        :param userid: The userid of the user to add
        :param username: The username of the user to add
        :param profile_pic_url: The profile picture url of the user to add
        :param session: The Instaloader session data of the user converted into a json string

        """

        c = self.conn.cursor()
        c.execute(
            """
            INSERT INTO users (userid, username, profile_pic_url, session)
            VALUES (?, ?, ?, ?)
            """,
            (userid, username, profile_pic_url, session),
        )
        self.conn.commit()

    def delete_user(self, userid: str) -> None:
        """
        Deletes an user from the database. Effectively logging them out of the application.

        :param userid: The userid of the user to delete
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE userid=?", (userid,))
        self.conn.commit()

    def get_users(self) -> List[Tuple[str, str, str, str]]:
        """
        Gets all the Instagram users from the database.


        :return: A list of all the instagram users that are logged into the application
        """
        c = self.conn.cursor()
        c.execute("SELECT * FROM users")
        return c.fetchall()
