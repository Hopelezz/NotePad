from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
)


class SettingsDialog(QDialog):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # User Information
        user = self.db.get_user(user_id)
        self.username_input = QLineEdit(user[1])
        self.email_input = QLineEdit(user[2])

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)

        # Theme Selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        current_theme = self.db.get_user_settings(user_id)
        self.theme_combo.setCurrentText(current_theme.capitalize())

        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.theme_combo)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_settings(self):
        username = self.username_input.text()
        email = self.email_input.text()
        theme = self.theme_combo.currentText().lower()

        # Update user information
        self.db.update_user(self.user_id, username, email)

        # Update user settings
        self.db.update_user_settings(self.user_id, theme)

        # Log the activity
        self.db.log_activity(self.user_id, "updated_settings")

        self.accept()
