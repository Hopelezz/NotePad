import sqlite3
import bcrypt


class Database:
    def __init__(self, db_name="notes.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            target TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            theme TEXT DEFAULT 'light',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        )

        self.conn.commit()

    def close(self):
        self.conn.close()

    def create_user(self, username, password, email):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.cursor.execute(
            """
        INSERT INTO users (username, password_hash, email)
        VALUES (?, ?, ?)
        """,
            (username, hashed, email),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def authenticate_user(self, username, password):
        self.cursor.execute(
            "SELECT id, password_hash FROM users WHERE username = ?", (username,)
        )
        user = self.cursor.fetchone()
        if user and bcrypt.checkpw(password.encode("utf-8"), user[1]):
            return user[0]
        return None

    def get_user(self, user_id):
        self.cursor.execute(
            "SELECT id, username, email FROM users WHERE id = ?", (user_id,)
        )
        return self.cursor.fetchone()

    def update_user(self, user_id, username, email):
        self.cursor.execute(
            """
        UPDATE users SET username = ?, email = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
            (username, email, user_id),
        )
        self.conn.commit()

    def log_activity(self, user_id, action, target=None):
        self.cursor.execute(
            """
        INSERT INTO activity_logs (user_id, action, target)
        VALUES (?, ?, ?)
        """,
            (user_id, action, target),
        )
        self.conn.commit()

    def get_user_settings(self, user_id):
        self.cursor.execute(
            "SELECT theme FROM user_settings WHERE user_id = ?", (user_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else "light"

    def update_user_settings(self, user_id, theme):
        self.cursor.execute(
            """
        INSERT OR REPLACE INTO user_settings (user_id, theme)
        VALUES (?, ?)
        """,
            (user_id, theme),
        )
        self.conn.commit()
