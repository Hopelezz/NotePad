from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QListWidget, QTextEdit, QPushButton, QListWidgetItem, 
                           QSplitter, QMessageBox)
from PyQt6.QtCore import Qt
from note import Note

class MainWindow(QMainWindow):
  def __init__(self):
      super().__init__()
      self.setWindowTitle("Notepad App")
      self.setGeometry(100, 100, 800, 600)

      self.central_widget = QWidget()
      self.setCentralWidget(self.central_widget)

      self.layout = QHBoxLayout(self.central_widget)

      self.splitter = QSplitter(Qt.Orientation.Horizontal)

      self.note_list = QListWidget()
      self.note_list.itemClicked.connect(self.load_note)
      self.note_list.itemChanged.connect(self.rename_note)

      self.note_editor = QTextEdit()
      self.note_editor.textChanged.connect(self.save_note)

      self.splitter.addWidget(self.note_list)
      self.splitter.addWidget(self.note_editor)

      self.splitter.setSizes([200, 600])

      self.button_layout = QVBoxLayout()
      self.new_button = QPushButton("New Note")
      self.new_button.clicked.connect(self.new_note)
      self.delete_button = QPushButton("Delete Note")
      self.delete_button.clicked.connect(self.delete_note)

      self.button_layout.addWidget(self.new_button)
      self.button_layout.addWidget(self.delete_button)
      self.button_layout.addStretch()

      self.layout.addWidget(self.splitter)
      self.layout.addLayout(self.button_layout)

      self.current_note = None
      self.load_notes()

  def load_notes(self):
      self.note_list.clear()
      for note in Note.get_all():
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
              self.note_editor.blockSignals(True)  # Prevent triggering save_note
              self.note_editor.setText(note.content)
              self.note_editor.blockSignals(False)
          else:
              QMessageBox.warning(self, "Error", "Could not load the selected note.")
      else:
          self.note_editor.clear()
          self.current_note = None

  def rename_note(self, item):
      if self.current_note and item.text() != self.current_note.title:
          self.current_note.title = item.text()
          self.current_note.update()

  def new_note(self):
      title = "New Note"
      note = Note.create(title, "")
      self.load_notes()
      self.current_note = note
      self.note_editor.clear()
      
      for i in range(self.note_list.count()):
          item = self.note_list.item(i)
          if item.data(Qt.ItemDataRole.UserRole) == note.id:
              self.note_list.editItem(item)
              break

  def save_note(self):
      if self.current_note:
          self.current_note.content = self.note_editor.toPlainText()
          self.current_note.update()
          print(f"Saved note: {self.current_note.title}")  # Optional: for debugging

  def delete_note(self):
      if self.current_note:
          self.current_note.delete()
          self.current_note = None
          self.note_editor.clear()
          self.load_notes()