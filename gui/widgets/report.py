from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QFrame, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from utils import logger

class ReportWidget(QFrame):
    formatRequested = Signal()
    exportRequested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(350)
        self._setup_ui()
        self._setup_style()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.title_label = QLabel("检查报告")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #424242;")
        layout.addWidget(self.title_label)

        self.summary_widget = QWidget()
        self.summary_layout = QHBoxLayout(self.summary_widget)
        self.summary_layout.setContentsMargins(0, 5, 0, 10)

        self.error_count = QLabel("❌ 错误: 0")
        self.error_count.setStyleSheet("color: #F44336; font-weight: bold;")
        self.summary_layout.addWidget(self.error_count)

        self.warning_count = QLabel("⚠️ 警告: 0")
        self.warning_count.setStyleSheet("color: #FF9800; font-weight: bold;")
        self.summary_layout.addWidget(self.warning_count)

        self.info_count = QLabel("ℹ️ 提示: 0")
        self.info_count.setStyleSheet("color: #2196F3; font-weight: bold;")
        self.summary_layout.addWidget(self.info_count)

        self.summary_layout.addStretch()
        layout.addWidget(self.summary_widget)

        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setPlaceholderText("检查报告将显示在这里...")
        layout.addWidget(self.report_text)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()

        self.format_btn = QPushButton("开始格式化")
        self.format_btn.clicked.connect(self.formatRequested.emit)
        self.format_btn.setEnabled(False)
        self.button_layout.addWidget(self.format_btn)

        self.export_btn = QPushButton("导出报告")
        self.export_btn.clicked.connect(self.exportRequested.emit)
        self.export_btn.setEnabled(False)
        self.button_layout.addWidget(self.export_btn)

        layout.addLayout(self.button_layout)

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
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)

    def set_results(self, results, summary: dict):
        try:
            logger.debug(f"ReportWidget.set_results: 开始更新, 问题总数: {summary.get('total', 0)}")
            self.error_count.setText(f"❌ 错误: {summary.get('error', 0)}")
            self.warning_count.setText(f"⚠️ 警告: {summary.get('warning', 0)}")
            self.info_count.setText(f"ℹ️ 提示: {summary.get('info', 0)}")

            if summary.get('total', 0) == 0:
                logger.debug("ReportWidget.set_results: 无问题, 显示成功提示")
                self.report_text.setHtml("<p style='color: #4CAF50; font-weight: bold;'>✅ 未发现问题，文档格式符合标准</p>")
                self.format_btn.setEnabled(False)
                self.export_btn.setEnabled(False)
            else:
                logger.debug(f"ReportWidget.set_results: 处理 {len(results)} 个具体问题")
                html_parts = []

                for result in results:
                    if result.level == 'error':
                        icon = "❌"
                        color = "#F44336"
                    elif result.level == 'warning':
                        icon = "⚠️"
                        color = "#FF9800"
                    else:
                        icon = "ℹ️"
                        color = "#2196F3"

                    html_parts.append(f"<p style='margin: 5px 0;'><span style='color: {color};'>{icon}</span> {result.message}</p>")

                    if result.suggestion:
                        html_parts.append(f"<p style='margin: 2px 0 10px 20px; color: #757575;'>→ 建议: {result.suggestion}</p>")

                html_content = "<br>".join(html_parts)
                self.report_text.setHtml(html_content)
                self.format_btn.setEnabled(True)
                self.export_btn.setEnabled(True)
                logger.debug("ReportWidget.set_results: HTML 报告更新完成")
        except Exception as e:
            logger.error(f"ReportWidget.set_results 异常: {e}", exc_info=True)


    def clear(self):
        self.error_count.setText("❌ 错误: 0")
        self.warning_count.setText("⚠️ 警告: 0")
        self.info_count.setText("ℹ️ 提示: 0")
        self.report_text.clear()
        self.format_btn.setEnabled(False)
        self.export_btn.setEnabled(False)

    def get_report_text(self) -> str:
        return self.report_text.toPlainText()
