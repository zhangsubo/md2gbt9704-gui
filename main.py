#!/usr/bin/env python3
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QWindow

from gui import MainWindow, theme
from utils import logger


def main():
    logger.info("=" * 50)
    logger.info("md2gbt9704 启动")

    QApplication.setApplicationName("md2gbt9704")
    QApplication.setApplicationVersion("1.0.0")
    QApplication.setOrganizationName("md2gbt9704")

    app = QApplication(sys.argv)

    logger.debug(f"平台: {app.platformName()}")
    logger.debug(f"屏幕数量: {len(app.screens())}")
    logger.debug(f"启动目录: {os.getcwd()}")

    app.setStyle('Fusion')

    is_dark = app.property("theme") == "dark"
    if not is_dark:
        is_dark = app.platformName() in ('xcb', 'offscreen')

    app.setPalette(theme.create_palette(is_dark))
    logger.debug(f"主题: {'深色' if is_dark else '浅色'}")

    window = MainWindow()
    window.show()
    window.raise_()
    window.activateWindow()

    logger.info("主窗口已显示")

    sys.exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"程序异常退出: {e}", exc_info=True)
        raise
