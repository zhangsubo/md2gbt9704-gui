from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal, QMimeData
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont

class FileDropWidget(QFrame):
    fileSelected = Signal(str)
    fileCleared = Signal()

    def __init__(self, parent=None, file_type="文件"):
        super().__init__(parent)
        self.file_type = file_type
        self.current_file = None
        self._setup_ui()
        self._setup_style()

    def _setup_ui(self):
        self.setAcceptDrops(True)
        self.setMinimumHeight(150)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.icon_label = QLabel("📄")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.icon_label)

        self.drop_label = QLabel(f"拖拽 {self.file_type} 到此处\n或点击选择文件")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setStyleSheet("color: #757575; font-size: 14px;")
        layout.addWidget(self.drop_label)

        self.file_label = QLabel("")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("color: #1976D2; font-size: 12px;")
        self.file_label.setVisible(False)
        layout.addWidget(self.file_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()

        self.select_btn = QPushButton("选择文件")
        self.select_btn.clicked.connect(self._on_select_clicked)
        self.button_layout.addWidget(self.select_btn)

        self.clear_btn = QPushButton("移除")
        self.clear_btn.clicked.connect(self._on_clear_clicked)
        self.clear_btn.setVisible(False)
        self.button_layout.addWidget(self.clear_btn)

        self.button_layout.addStretch()
        layout.addLayout(self.button_layout)

        self._update_file_label()

    def _setup_style(self):
        self.setStyleSheet("""
            QFrame {
                border: 2px dashed #E0E0E0;
                border-radius: 8px;
                background-color: #FAFAFA;
            }
            QFrame:hover {
                border-color: #1976D2;
                background-color: #E3F2FD;
            }
        """)

    def _on_select_clicked(self):
        from PySide6.QtWidgets import QFileDialog

        if self.file_type == "Markdown":
            filters = "Markdown 文件 (*.md *.markdown);;所有文件 (*.*)"
        elif self.file_type == "Word":
            filters = "Word 文档 (*.docx);;所有文件 (*.*)"
        else:
            filters = "所有支持的文件 (*.md *.docx);;所有文件 (*.*)"

        file_path, _ = QFileDialog.getOpenFileName(
            self, f"选择{self.file_type}", "", filters
        )

        if file_path:
            self.set_file(file_path)

    def _on_clear_clicked(self):
        self.clear()

    def set_file(self, file_path: str):
        self.current_file = file_path
        self.fileSelected.emit(file_path)
        self._update_file_label()

    def clear(self):
        self.current_file = None
        self.fileCleared.emit()
        self._update_file_label()

    def _update_file_label(self):
        if self.current_file:
            from pathlib import Path
            file_name = Path(self.current_file).name
            self.file_label.setText(f"已选择: {file_name}")
            self.file_label.setVisible(True)
            self.clear_btn.setVisible(True)
            self.drop_label.setVisible(False)
            self.icon_label.setText("✅")
        else:
            self.file_label.setVisible(False)
            self.clear_btn.setVisible(False)
            self.drop_label.setVisible(True)
            self.icon_label.setText("📄")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    border: 2px solid #1976D2;
                    border-radius: 8px;
                    background-color: #E3F2FD;
                }
            """)

    def dragLeaveEvent(self, event):
        self._setup_style()

    def dropEvent(self, event: QDropEvent):
        self._setup_style()
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path:
                self.set_file(file_path)

    def get_file_path(self) -> str:
        return self.current_file
