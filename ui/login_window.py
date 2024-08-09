from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt, QSettings
import jwt
from jwt import encode, decode
from datetime import datetime, timedelta, timezone

from secret_key import SECRET_KEY


class LoginWindow(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_user = None
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)

        self.remember_me = QCheckBox("Remember me")
        layout.addWidget(self.remember_me)

        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_id = self.db.authenticate_user(username, password)
        if user_id:
            self.current_user = self.db.get_user(user_id)
            if self.remember_me.isChecked():
                self.create_and_store_token(user_id)
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def create_and_store_token(self, user_id):
        expiration = datetime.now(timezone.utc) + timedelta(
            days=7
        )  # Token valid for 7 days
        token = jwt.encode(
            {"user_id": user_id, "exp": expiration}, SECRET_KEY, algorithm="HS256"
        )

        settings = QSettings("YourCompany", "NotepadApp")
        settings.setValue("user_token", token)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            try:
                user_id = self.db.create_user(
                    username, password, f"{username}@example.com"
                )
                self.current_user = self.db.get_user(user_id)
                QMessageBox.information(
                    self,
                    "Registration Successful",
                    "You can now log in with your new account.",
                )
            except Exception as e:
                QMessageBox.warning(self, "Registration Failed", str(e))
        else:
            QMessageBox.warning(
                self, "Registration Failed", "Please enter both username and password."
            )
