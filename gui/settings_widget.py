from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QSpinBox, QComboBox, QPushButton,
                               QGroupBox, QFormLayout, QScrollArea, QFrame,
                               QCheckBox)
from PySide6.QtCore import Qt, Signal, QThread
from pathlib import Path

from converter import config, get_all_font_options, check_all_required_fonts
from utils import logger

class FontDetector(QThread):
    fonts_detected = Signal(list)
    font_status_checked = Signal(dict)

    def run(self):
        logger.debug("FontDetector: 开始检测所有字体")
        all_fonts = get_all_font_options()
        self.fonts_detected.emit(all_fonts)
        logger.debug("FontDetector: 所有字体检测完成")

        logger.debug("FontDetector: 开始检查所需字体状态")
        font_status = check_all_required_fonts()
        self.font_status_checked.emit(font_status)
        logger.debug("FontDetector: 所需字体状态检查完成")


class SettingsWidget(QWidget):
    settingsChanged = Signal()

    def __init__(self, parent=None):
        logger.debug("SettingsWidget: __init__ 开始")
        super().__init__(parent)
        logger.debug("SettingsWidget: super().__init__ 完成")
        self.font_detector_thread = FontDetector()
        self.font_detector_thread.fonts_detected.connect(self._update_font_options)
        self.font_detector_thread.font_status_checked.connect(self._update_font_status_label)
        self._setup_ui()
        # self._load_settings() # Removed as it's called after font detection in _update_font_options
        self.font_detector_thread.start()
        logger.debug("SettingsWidget: __init__ 完成")

    def _setup_ui(self):
        logger.debug("SettingsWidget._setup_ui: 开始")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        logger.debug("SettingsWidget._setup_ui: 创建 margin group")
        self._create_margin_group(scroll_layout)
        logger.debug("SettingsWidget._setup_ui: 创建 font group")
        self._create_font_group(scroll_layout)
        logger.debug("SettingsWidget._setup_ui: 创建 preset group")
        self._create_preset_group(scroll_layout)
        logger.debug("SettingsWidget._setup_ui: 创建 logging group")
        self._create_logging_group(scroll_layout)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        self._create_button_bar(main_layout)
        logger.debug("SettingsWidget._setup_ui: 完成")

    def _create_margin_group(self, parent_layout):
        logger.debug("SettingsWidget._create_margin_group: 开始")
        group = QGroupBox("页边距设置")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        layout = QFormLayout(group)

        self.margin_top = QSpinBox()
        self.margin_top.setRange(20, 50)
        self.margin_top.setSuffix(" mm")
        self.margin_top.valueChanged.connect(self._on_margin_changed)
        layout.addRow("上边距:", self.margin_top)

        self.margin_bottom = QSpinBox()
        self.margin_bottom.setRange(20, 50)
        self.margin_bottom.setSuffix(" mm")
        self.margin_bottom.valueChanged.connect(self._on_margin_changed)
        layout.addRow("下边距:", self.margin_bottom)

        self.margin_left = QSpinBox()
        self.margin_left.setRange(20, 50)
        self.margin_left.setSuffix(" mm")
        self.margin_left.valueChanged.connect(self._on_margin_changed)
        layout.addRow("左边距:", self.margin_left)

        self.margin_right = QSpinBox()
        self.margin_right.setRange(20, 50)
        self.margin_right.setSuffix(" mm")
        self.margin_right.valueChanged.connect(self._on_margin_changed)
        layout.addRow("右边距:", self.margin_right)

        parent_layout.addWidget(group)
        logger.debug("SettingsWidget._create_margin_group: 完成")

    def _create_font_group(self, parent_layout):
        logger.debug("SettingsWidget._create_font_group: 开始")
        group = QGroupBox("字体设置")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        layout = QFormLayout(group)

        # Initial empty font options, will be updated by thread
        empty_font_options = ["检测中..."]

        self.font_title = QComboBox()
        self.font_title.addItems(empty_font_options)
        self.font_title.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("主标题:", self.font_title)

        self.font_h1 = QComboBox()
        self.font_h1.addItems(empty_font_options)
        self.font_h1.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("一级标题 (一、):", self.font_h1)

        self.font_h2 = QComboBox()
        self.font_h2.addItems(empty_font_options)
        self.font_h2.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("二级标题 (（一）):", self.font_h2)

        self.font_h3 = QComboBox()
        self.font_h3.addItems(empty_font_options)
        self.font_h3.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("三级标题 (1.):", self.font_h3)

        self.font_h4 = QComboBox()
        self.font_h4.addItems(empty_font_options)
        self.font_h4.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("四级标题 (（1）):", self.font_h4)

        self.font_body = QComboBox()
        self.font_body.addItems(empty_font_options)
        self.font_body.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("正文:", self.font_body)

        self.font_table = QComboBox()
        self.font_table.addItems(empty_font_options)
        self.font_table.currentTextChanged.connect(self._on_font_changed)
        layout.addRow("表格:", self.font_table)

        parent_layout.addWidget(group)

        self.font_status_label = QLabel("字体检测中...")
        self.font_status_label.setStyleSheet("color: #757575; font-size: 12px;")
        parent_layout.addWidget(self.font_status_label)
        logger.debug("SettingsWidget._create_font_group: 完成")

    def _update_font_options(self, font_options):
        logger.debug(f"SettingsWidget: 更新字体选项, 数量: {len(font_options)}")
        for combo_box in [self.font_title, self.font_h1, self.font_h2, self.font_h3,
                         self.font_h4, self.font_body, self.font_table]:
            combo_box.clear()
            combo_box.addItems(font_options)
        self._load_settings() # Reload settings to apply selected fonts

    def _update_font_status_label(self, font_status):
        logger.debug("SettingsWidget: 更新字体状态标签")
        missing_fonts = [font for font, (installed, _) in font_status.items() if not installed]
        if missing_fonts:
            self.font_status_label.setText(f"警告: 缺少字体: {', '.join(missing_fonts)}")
            self.font_status_label.setStyleSheet("color: red; font-size: 12px;")
        else:
            self.font_status_label.setText("所有所需字体均已安装。")
            self.font_status_label.setStyleSheet("color: green; font-size: 12px;")

    def _create_preset_group(self, parent_layout):
        logger.debug("SettingsWidget._create_preset_group: 开始")
        group = QGroupBox("预设管理")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        layout = QHBoxLayout(group)

        self.preset_combo = QComboBox()
        self.preset_combo.addItem("GB/T 9704-2012（党政机关公文格式）", "gbt9704")
        self.preset_combo.addItem("国家行政机关公文格式", "administration")
        self.preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        layout.addWidget(self.preset_combo)

        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        self.reset_btn.clicked.connect(self._on_reset_clicked)
        layout.addWidget(self.reset_btn)

        parent_layout.addWidget(group)
        logger.debug("SettingsWidget._create_preset_group: 完成")

    def _create_logging_group(self, parent_layout):
        logger.debug("SettingsWidget._create_logging_group: 开始")
        group = QGroupBox("日志设置")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        layout = QVBoxLayout(group)
        self.enable_desktop_logging_checkbox = QCheckBox("启用桌面日志文件 (md2gbt9704_日期.log)")
        self.enable_desktop_logging_checkbox.stateChanged.connect(self._on_enable_desktop_logging_changed)
        layout.addWidget(self.enable_desktop_logging_checkbox)
        parent_layout.addWidget(group)
        logger.debug("SettingsWidget._create_logging_group: 完成")

    def _create_button_bar(self, main_layout):
        logger.debug("SettingsWidget._create_button_bar: 开始")
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.apply_btn = QPushButton("应用设置")
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 24px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.apply_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(self.apply_btn)

        main_layout.addLayout(button_layout)
        logger.debug("SettingsWidget._create_button_bar: 完成")

    def _load_settings(self):
        logger.debug("SettingsWidget: 加载设置")
        self.margin_top.setValue(config.get('margin_top', 30))
        self.margin_bottom.setValue(config.get('margin_bottom', 30))
        self.margin_left.setValue(config.get('margin_left', 28))
        self.margin_right.setValue(config.get('margin_right', 26))

        fonts = config.get_fonts()
        self.font_title.setCurrentText(fonts.get("title", "方正小标宋简体"))
        self.font_h1.setCurrentText(fonts.get("heading1", "黑体"))
        self.font_h2.setCurrentText(fonts.get("heading2", "楷体"))
        self.font_h3.setCurrentText(fonts.get("heading3", "仿宋"))
        self.font_h4.setCurrentText(fonts.get("heading4", "仿宋"))
        self.font_body.setCurrentText(fonts.get("body", "仿宋"))
        self.font_table.setCurrentText(fonts.get("table", "仿宋"))
        self.enable_desktop_logging_checkbox.setChecked(config.get_enable_desktop_logging())

    def _on_margin_changed(self):
        logger.debug("SettingsWidget: 边距设置已更改")
        self.settingsChanged.emit()

    def _on_font_changed(self):
        logger.debug("SettingsWidget: 字体设置已更改")
        self.settingsChanged.emit()

    def _on_preset_changed(self):
        logger.debug("SettingsWidget: 预设已更改")
        preset_name = self.preset_combo.currentData()
        if preset_name and preset_name in config.PRESETS:
            preset = config.PRESETS[preset_name]
            self.margin_top.setValue(preset["margins"]["top"])
            self.margin_bottom.setValue(preset["margins"]["bottom"])
            self.margin_left.setValue(preset["margins"]["left"])
            self.margin_right.setValue(preset["margins"]["right"])
        self.settingsChanged.emit()

    def _on_enable_desktop_logging_changed(self, state):
        logger.debug(f"SettingsWidget: 桌面日志开关状态改变为 {state}")
        config.set_enable_desktop_logging(state == Qt.CheckState.Checked)
        self.settingsChanged.emit()

    def _on_reset_clicked(self):
        logger.debug("SettingsWidget: 恢复默认设置")
        config.reset_to_default()
        self._load_settings()
        self.settingsChanged.emit()

    def _save_settings(self):
        logger.debug("SettingsWidget: 保存设置")
        margins = {
            "top": self.margin_top.value(),
            "bottom": self.margin_bottom.value(),
            "left": self.margin_left.value(),
            "right": self.margin_right.value(),
        }
        config.set_margins(margins)

        fonts = {
            "title": self.font_title.currentText(),
            "heading1": self.font_h1.currentText(),
            "heading2": self.font_h2.currentText(),
            "heading3": self.font_h3.currentText(),
            "heading4": self.font_h4.currentText(),
            "body": self.font_body.currentText(),
            "table": self.font_table.currentText(),
        }
        config.set_fonts(fonts)

        self.settingsChanged.emit()
