import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from ui.main_window import MainWindow
from ui.login_window import LoginWindow
from database import Database
import jwt
from secret_key import SECRET_KEY


def get_user_from_token(db):
    settings = QSettings("YourCompany", "NotepadApp")
    token = settings.value("user_token")

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload["user_id"]
            return db.get_user(user_id)
        except jwt.ExpiredSignatureError:
            settings.remove("user_token")  # Remove expired token
        except jwt.InvalidTokenError:
            settings.remove("user_token")  # Remove invalid token

    return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Database()

    user = get_user_from_token(db)

    if user:
        window = MainWindow(db, user)
        window.show()
    else:
        login_window = LoginWindow(db)
        if login_window.exec():
            window = MainWindow(db, login_window.current_user)
            window.show()
        else:
            sys.exit()

    sys.exit(app.exec())
