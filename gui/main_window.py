import os
import sys
import threading
from pathlib import Path
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QTabWidget, QLabel, QPushButton, QLineEdit,
                               QFileDialog, QMessageBox, QStatusBar, QToolBar,
                               QApplication)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QAction, QKeySequence

from converter import MarkdownConverter, FormatChecker, FormatFormatter, config
from .widgets import FileDropWidget, PreviewWidget, ReportWidget
from .settings_widget import SettingsWidget
from utils import logger


class MainWindow(QMainWindow):
    # Signals for thread-safe UI updates
    check_finished = Signal(list, dict)
    format_finished = Signal(bool, str)

    def __init__(self):
        logger.debug("MainWindow: 开始初始化")
        super().__init__()
        logger.debug("MainWindow: super().__init__ 完成")
        self.current_file = None
        self.output_dir = str(Path.home() / "Desktop")
        self._setup_ui()
        self._setup_toolbar()
        self._connect_signals()
        self._update_status_bar()
        logger.debug("MainWindow: 初始化完成")

    def _setup_ui(self):
        logger.debug("MainWindow._setup_ui: 开始")
        self.setWindowTitle("md2gbt9704 - 公文格式工具")
        self.setMinimumSize(900, 700)
        self.resize(1000, 750)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 5)

        self.tab_widget = QTabWidget()
        logger.debug("MainWindow._setup_ui: 创建标签页")
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
            QTabBar::tab {
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1976D2;
                color: white;
            }
        """)

        self._create_convert_tab()
        self._create_check_tab()
        self._create_format_tab()
        self._create_settings_tab()

        main_layout.addWidget(self.tab_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("就绪")
        self.status_bar.addPermanentWidget(self.status_label)
        self.preset_label = QLabel(f"当前预设: {config.PRESETS.get(config.get('preset', 'gbt9704'), {}).get('name', 'GB/T 9704-2012')}")
        self.status_bar.addPermanentWidget(self.preset_label)

    def _setup_toolbar(self):
        toolbar = QToolBar("主工具栏")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_action = QAction("📂 打开", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._on_open_file)
        toolbar.addAction(open_action)

        toolbar.addSeparator()

        settings_action = QAction("⚙️ 设置", self)
        settings_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(3))
        toolbar.addAction(settings_action)

    def _create_convert_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        header = QLabel("Markdown → DOCX 转换")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2;")
        layout.addWidget(header)

        desc = QLabel("将 Markdown 文档按照 GB/T 9704-2012 标准转换为标准公文格式")
        desc.setStyleSheet("color: #757575; font-size: 12px;")
        layout.addWidget(desc)

        self.convert_file_drop = FileDropWidget(file_type="Markdown")
        self.convert_file_drop.fileSelected.connect(self._on_convert_file_selected)
        layout.addWidget(self.convert_file_drop)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.convert_output_path = QLineEdit()
        self.convert_output_path.setText(self.output_dir)
        self.convert_output_path.setReadOnly(True)
        output_layout.addWidget(self.convert_output_path)

        output_browse_btn = QPushButton("浏览...")
        output_browse_btn.clicked.connect(self._on_browse_output)
        output_layout.addWidget(output_browse_btn)
        layout.addLayout(output_layout)

        layout.addStretch()

        self.convert_preview = PreviewWidget()
        layout.addWidget(self.convert_preview)

        self.convert_btn = QPushButton("🔄 开始转换")
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.convert_btn.clicked.connect(self._on_convert)
        self.convert_btn.setEnabled(False)
        layout.addWidget(self.convert_btn)

        self.tab_widget.addTab(tab, "📝 MD转DOCX")

    def _create_check_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        header = QLabel("DOCX 格式检查")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2;")
        layout.addWidget(header)

        desc = QLabel("检查 Word 文档是否符合 GB/T 9704-2012 公文格式标准")
        desc.setStyleSheet("color: #757575; font-size: 12px;")
        layout.addWidget(desc)

        self.check_file_drop = FileDropWidget(file_type="Word")
        self.check_file_drop.fileSelected.connect(self._on_check_file_selected)
        layout.addWidget(self.check_file_drop)

        self.check_report = ReportWidget()
        self.check_report.formatRequested.connect(self._on_format_from_check)
        layout.addWidget(self.check_report)

        layout.addStretch()

        self.check_btn = QPushButton("🔍 开始检查")
        self.check_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.check_btn.clicked.connect(self._on_check)
        self.check_btn.setEnabled(False)
        layout.addWidget(self.check_btn)

        self.tab_widget.addTab(tab, "🔍 格式检查")

    def _create_format_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        header = QLabel("DOCX 格式标准化")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #1976D2;")
        layout.addWidget(header)

        desc = QLabel("自动将 Word 文档按照 GB/T 9704-2012 标准进行格式化")
        desc.setStyleSheet("color: #757575; font-size: 12px;")
        layout.addWidget(desc)

        self.format_file_drop = FileDropWidget(file_type="Word")
        self.format_file_drop.fileSelected.connect(self._on_format_file_selected)
        layout.addWidget(self.format_file_drop)

        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        self.format_output_path = QLineEdit()
        self.format_output_path.setText(self.output_dir)
        self.format_output_path.setReadOnly(True)
        output_layout.addWidget(self.format_output_path)

        output_browse_btn = QPushButton("浏览...")
        output_browse_btn.clicked.connect(self._on_browse_format_output)
        output_layout.addWidget(output_browse_btn)
        layout.addLayout(output_layout)

        layout.addStretch()

        self.format_btn = QPushButton("🔧 开始格式化")
        self.format_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
        """)
        self.format_btn.clicked.connect(self._on_format)
        self.format_btn.setEnabled(False)
        layout.addWidget(self.format_btn)

        self.tab_widget.addTab(tab, "🔧 格式标准化")

    def _create_settings_tab(self):
        logger.debug("MainWindow._create_settings_tab: 开始")
        self.settings_widget = SettingsWidget()
        logger.debug("MainWindow._create_settings_tab: SettingsWidget 创建完成")
        self.settings_widget.settingsChanged.connect(self._on_settings_changed)
        self.tab_widget.addTab(self.settings_widget, "⚙️ 设置")
        logger.debug("MainWindow._create_settings_tab: 完成")

    def _connect_signals(self):
        self.convert_file_drop.fileCleared.connect(lambda: self.convert_btn.setEnabled(False))
        self.check_file_drop.fileCleared.connect(lambda: self.check_btn.setEnabled(False))
        self.format_file_drop.fileCleared.connect(lambda: self.format_btn.setEnabled(False))
        self.check_finished.connect(self._on_check_complete)
        self.format_finished.connect(self._on_format_complete)

    def _update_status_bar(self):
        preset_name = config.PRESETS.get(config.get('preset', 'gbt9704'), {}).get('name', 'GB/T 9704-2012')
        self.preset_label.setText(f"当前预设: {preset_name}")

    def _on_open_file(self):
        logger.log_operation("打开文件对话框")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "",
            "支持的文件 (*.md *.docx);;所有文件 (*.*)"
        )
        if file_path:
            logger.log_operation("选择文件", file_path)
            ext = Path(file_path).suffix.lower()
            if ext in ['.md', '.markdown']:
                self.tab_widget.setCurrentIndex(0)
                self.convert_file_drop.set_file(file_path)
            else:
                self.tab_widget.setCurrentIndex(1)
                self.check_file_drop.set_file(file_path)

    def _on_convert_file_selected(self, file_path):
        logger.log_operation("选择MD文件", file_path)
        self.current_file = file_path
        self.convert_btn.setEnabled(True)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.convert_preview.set_content(content)
        except Exception as e:
            logger.error(f"读取文件失败: {str(e)}")
            self.convert_preview.set_content(f"读取文件失败: {str(e)}")

    def _on_check_file_selected(self, file_path):
        logger.log_operation("选择检查文件", file_path)
        self.current_file = file_path
        self.check_btn.setEnabled(True)
        self.check_report.clear()

    def _on_format_file_selected(self, file_path):
        logger.log_operation("选择格式化文件", file_path)
        self.current_file = file_path
        self.format_btn.setEnabled(True)

    def _on_browse_output(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录", self.output_dir)
        if dir_path:
            self.output_dir = dir_path
            self.convert_output_path.setText(dir_path)

    def _on_browse_format_output(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录", self.output_dir)
        if dir_path:
            self.output_dir = dir_path
            self.format_output_path.setText(dir_path)

    def _on_convert(self):
        if not self.current_file:
            return

        logger.log_operation("开始MD转DOCX")
        input_path = self.current_file
        file_name = Path(input_path).stem
        output_path = os.path.join(self.output_dir, f"{file_name}_format.docx")

        logger.debug(f"输入: {input_path}, 输出: {output_path}")

        reply = QMessageBox.question(
            self, "确认", f"输出文件将保存为:\n{output_path}",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        if reply != QMessageBox.StandardButton.Ok:
            logger.info("用户取消转换")
            return

        self._run_conversion(input_path, output_path)

    def _run_conversion(self, input_path, output_path):
        self.convert_btn.setEnabled(False)
        self.status_label.setText("正在转换...")
        logger.info("开始转换线程")

        def progress(msg, percent):
            # Move UI updates to main thread
            QTimer.singleShot(0, lambda: self.status_label.setText(msg))
            logger.debug(f"进度: {msg}")

        converter = MarkdownConverter(progress_callback=progress)

        def do_convert():
            try:
                logger.info(f"转换中: {input_path}")
                success = converter.convert_file(input_path, output_path)

                def on_complete():
                    if success:
                        logger.info(f"转换成功: {output_path}")
                        self.status_label.setText(f"转换完成: {Path(output_path).name}")
                        reply = QMessageBox.information(
                            self, "转换成功",
                            f"文件已保存到:\n{output_path}\n\n是否打开文件？",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply == QMessageBox.StandardButton.Yes:
                            os.startfile(output_path) if sys.platform == 'win32' else os.system(f'open "{output_path}"')
                    else:
                        logger.error("转换失败")
                        self.status_label.setText("转换失败")
                    self.convert_btn.setEnabled(True)

                QTimer.singleShot(0, on_complete)
            except Exception as e:
                logger.error(f"转换异常: {e}", exc_info=True)
                QTimer.singleShot(0, lambda: self.status_label.setText("转换失败"))
                QTimer.singleShot(0, lambda: self.convert_btn.setEnabled(True))

        thread = threading.Thread(target=do_convert)
        thread.start()

    def _on_check(self):
        if not self.current_file:
            return

        logger.log_operation("开始格式检查")
        self.check_btn.setEnabled(False)
        self.status_label.setText("正在检查...")

        def progress(msg, percent):
            # Move UI updates to main thread
            QTimer.singleShot(0, lambda: self.status_label.setText(msg))
            logger.debug(f"检查进度: {msg}")

        checker = FormatChecker(progress_callback=progress)

        def do_check():
            try:
                logger.info(f"检查中: {self.current_file}")
                results = checker.check_document(self.current_file)
                summary = checker.get_summary()
                
                logger.info(f"检查完成: {summary['error']} 错误, {summary['warning']} 警告")
                self.check_finished.emit(results, summary)
            except Exception as e:
                logger.error(f"检查异常: {e}", exc_info=True)
                QTimer.singleShot(0, lambda: self.status_label.setText("检查失败"))
                QTimer.singleShot(0, lambda: self.check_btn.setEnabled(True))

        thread = threading.Thread(target=do_check)
        thread.start()

    def _on_check_complete(self, results, summary):
        try:
            logger.debug("MainWindow._on_check_complete: 开始更新 UI")
            self.check_report.set_results(results, summary)
            self.status_label.setText(f"检查完成: {summary['total']} 个问题")
            self.check_btn.setEnabled(True)
            logger.debug("MainWindow._on_check_complete: UI 更新完成")
        except Exception as e:
            logger.error(f"MainWindow._on_check_complete 异常: {e}", exc_info=True)
            self.check_btn.setEnabled(True)

    def _on_format_from_check(self):
        self.tab_widget.setCurrentIndex(2)
        if self.current_file:
            self.format_file_drop.set_file(self.current_file)

    def _on_format(self):
        if not self.current_file:
            return

        logger.log_operation("开始格式标准化")
        input_path = self.current_file
        file_name = Path(input_path).stem
        output_path = os.path.join(self.output_dir, f"{file_name}_formatted.docx")

        logger.debug(f"输入: {input_path}, 输出: {output_path}")

        reply = QMessageBox.question(
            self, "确认", f"输出文件将保存为:\n{output_path}",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        if reply != QMessageBox.StandardButton.Ok:
            logger.info("用户取消格式化")
            return

        self._run_format(input_path, output_path)

    def _run_format(self, input_path, output_path):
        self.format_btn.setEnabled(False)
        self.status_label.setText("正在格式化...")
        logger.info("开始格式化线程")

        def progress(msg, percent):
            # Move UI updates to main thread
            QTimer.singleShot(0, lambda: self.status_label.setText(msg))
            logger.debug(f"进度: {msg}")

        formatter = FormatFormatter(progress_callback=progress)

        def do_format():
            try:
                logger.info(f"格式化中: {input_path}")
                success = formatter.format_document(input_path, output_path)
                self.format_finished.emit(success, output_path)
            except Exception as e:
                logger.error(f"格式化异常: {e}", exc_info=True)
                QTimer.singleShot(0, lambda: self.status_label.setText("格式化失败"))
                QTimer.singleShot(0, lambda: self.format_btn.setEnabled(True))

        thread = threading.Thread(target=do_format)
        thread.start()

    def _on_format_complete(self, success, output_path):
        if success:
            logger.info(f"格式化成功: {output_path}")
            self.status_label.setText(f"格式化完成: {Path(output_path).name}")
            reply = QMessageBox.information(
                self, "格式化成功",
                f"文件已保存到:\n{output_path}\n\n是否打开文件？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                os.startfile(output_path) if sys.platform == 'win32' else os.system(f'open "{output_path}"')
        else:
            logger.error("格式化失败")
            self.status_label.setText("格式化失败")
        self.format_btn.setEnabled(True)

    def _on_settings_changed(self):
        self._update_status_bar()
        self.status_label.setText("设置已保存")
        logger.log_operation("设置已保存")

    def closeEvent(self, event):
        logger.info("程序关闭")
        event.accept()
