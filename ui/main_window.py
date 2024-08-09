from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QTextEdit,
    QPushButton,
    QListWidgetItem,
    QSplitter,
    QMessageBox,
    QLabel,
)
from PyQt6.QtCore import Qt
from note import Note
from ui.settings_dialog import SettingsDialog
from ui.login_window import LoginWindow


class MainWindow(QMainWindow):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user
        self.setWindowTitle(f"Notepad App - {user[1]}")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Top bar with user info and buttons
        top_bar = QHBoxLayout()

        # User info
        self.user_label = QLabel(f"Logged in as: {user[1]}")
        top_bar.addWidget(self.user_label)

        # Add stretch to push buttons to the right
        top_bar.addStretch(1)

        # Buttons
        self.new_button = QPushButton("New Note")
        self.new_button.clicked.connect(self.new_note)
        self.delete_button = QPushButton("Delete Note")
        self.delete_button.clicked.connect(self.delete_note)
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)

        top_bar.addWidget(self.new_button)
        top_bar.addWidget(self.delete_button)
        top_bar.addWidget(self.settings_button)
        top_bar.addWidget(self.logout_button)

        self.layout.addLayout(top_bar)

        # Main content area
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.load_note)
        self.note_list.itemChanged.connect(self.rename_note)

        self.note_editor = QTextEdit()
        self.note_editor.textChanged.connect(self.save_note)

        self.splitter.addWidget(self.note_list)
        self.splitter.addWidget(self.note_editor)

        self.splitter.setSizes([200, 600])

        self.layout.addWidget(self.splitter)

        self.current_note = None
        self.load_notes()

        self.apply_theme()

    def load_notes(self):
        self.note_list.clear()
        for note in Note.get_all(self.user[0]):
            item = QListWidgetItem(note.title)
            item.setData(Qt.ItemDataRole.UserRole, note.id)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.note_list.addItem(item)

    def load_note(self, item):
        if item:
            note_id = item.data(Qt.ItemDataRole.UserRole)
            note = Note.get(note_id)
            if note:
                self.current_note = note
                self.note_editor.blockSignals(True)
                self.note_editor.setText(note.content)
                self.note_editor.blockSignals(False)
                self.db.log_activity(self.user[0], "opened_note", note.title)
            else:
                QMessageBox.warning(self, "Error", "Could not load the selected note.")
        else:
            self.note_editor.clear()
            self.current_note = None

    def rename_note(self, item):
        if self.current_note and item.text() != self.current_note.title:
            self.current_note.title = item.text()
            self.current_note.update()
            self.db.log_activity(self.user[0], "renamed_note", self.current_note.title)

    def new_note(self):
        title = "New Note"
        note = Note.create(title, "", self.user[0])
        self.load_notes()
        self.current_note = note
        self.note_editor.clear()
        self.db.log_activity(self.user[0], "created_note", title)

        for i in range(self.note_list.count()):
            item = self.note_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == note.id:
                self.note_list.editItem(item)
                break

    def save_note(self):
        if self.current_note:
            self.current_note.content = self.note_editor.toPlainText()
            self.current_note.update()
            self.db.log_activity(self.user[0], "edited_note", self.current_note.title)

    def delete_note(self):
        if self.current_note:
            title = self.current_note.title
            self.current_note.delete()
            self.current_note = None
            self.note_editor.clear()
            self.load_notes()
            self.db.log_activity(self.user[0], "deleted_note", title)

    def open_settings(self):
        dialog = SettingsDialog(self.db, self.user[0])
        if dialog.exec():
            self.apply_theme()

    def apply_theme(self):
        theme = self.db.get_user_settings(self.user[0])
        if theme == "dark":
            self.setStyleSheet(
                """
            QWidget { background-color: #2b2b2b; color: #ffff; }
            QTextEdit { background-color: #3c3f41; color: #ffff; border: 1px solid #5555; }
            QPushButton { background-color: #4c4c4c; color: #ffff; border: 1px solid #5555; padding: 5px; }
            QPushButton:hover { background-color: #5c5c5c; }
            QListWidget { background-color: #3c3f41; color: #ffff; border: 1px solid #5555; }
            QListWidget::item:selected { background-color: #4b6eaf; }
            """
            )
        else:
            self.setStyleSheet(
                """
            QWidget { background-color: #ffffff; color: #000000; }
            QTextEdit { background-color: #f0f0f0; color: #000000; border: 1px solid #cccccc; }
            QPushButton { background-color: #e0e0e0; color: #000000; border: 1px solid #cccccc; padding: 5px; }
            QPushButton:hover { background-color: #d0d0d0; }
            QListWidget { background-color: #f0f0f0; color: #000000; border: 1px solid #cccccc; }
            QListWidget::item:selected { background-color: #b8d0e8; }
            """
            )

    def logout(self):
        self.close()
        #   Show login Window
        login_window = LoginWindow(self.db)
        if login_window.exec():
            self.user = login_window.current_user
            self.setWindowTitle(f"Notepad App - {self.user[1]}")
            self.user_label.setText(f"Logged in as: {self.user[1]}")
            self.load_notes()
            self.apply_theme()
        else:
            self.close()
