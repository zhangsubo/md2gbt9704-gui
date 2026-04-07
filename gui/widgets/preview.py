from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class PreviewWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_style()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.title_label = QLabel("预览")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #424242;")
        layout.addWidget(self.title_label)

        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText("预览内容将显示在这里...")
        layout.addWidget(self.preview_text)

    def _setup_style(self):
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
            QTextEdit {
                border: none;
                background-color: transparent;
            }
        """)

    def set_content(self, content: str):
        self.preview_text.setPlainText(content)

    def append_content(self, content: str):
        current = self.preview_text.toPlainText()
        if current:
            self.preview_text.setPlainText(current + "\n" + content)
        else:
            self.preview_text.setPlainText(content)

    def clear(self):
        self.preview_text.clear()

    def get_content(self) -> str:
        return self.preview_text.toPlainText()
