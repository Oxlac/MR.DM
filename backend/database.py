import sqlite3


class DatabaseManager:
    """Manages Database Connection instance
    """    
    _instance = None
    """
    The singleton instance of the class
    """

    conn = None
    """
    Connection to the database
    """

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect("data.db")
            cls._instance.create_tables()
        return cls._instance

    def create_tables(self):
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

    def get_users(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users")
        return c.fetchall()

    def get_user(self, userid):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE userid=?", (userid,))
        return c.fetchone()

    def add_user(self, userid, username, profile_pic_url, session):
        c = self.conn.cursor()
        c.execute(
            """
            INSERT INTO users (userid, username, profile_pic_url, session)
            VALUES (?, ?, ?, ?)
            """,
            (userid, username, profile_pic_url, session),
        )
        self.conn.commit()

    def delete_user(self, userid):
        c = self.conn.cursor()
        c.execute("DELETE FROM users WHERE userid=?", (userid,))
        self.conn.commit()
