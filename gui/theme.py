from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette

class Theme:
    LIGHT_COLORS = {
        'primary': '#1976D2',
        'primary_dark': '#1565C0',
        'secondary': '#424242',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#F44336',
        'background': '#FAFAFA',
        'surface': '#FFFFFF',
        'text': '#212121',
        'text_secondary': '#757575',
        'border': '#E0E0E0',
        'hover': '#E3F2FD',
    }

    DARK_COLORS = {
        'primary': '#64B5F6',
        'primary_dark': '#42A5F5',
        'secondary': '#B0BEC5',
        'success': '#81C784',
        'warning': '#FFB74D',
        'error': '#E57373',
        'background': '#121212',
        'surface': '#1E1E1E',
        'text': '#FFFFFF',
        'text_secondary': '#B0B0B0',
        'border': '#424242',
        'hover': '#1E3A5F',
    }

    @staticmethod
    def get_theme(is_dark: bool = False) -> dict:
        if is_dark:
            return Theme.DARK_COLORS.copy()
        return Theme.LIGHT_COLORS.copy()

    @staticmethod
    def create_palette(is_dark: bool = False) -> QPalette:
        colors = Theme.get_theme(is_dark)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(colors['background']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors['text']))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors['surface']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors['surface']))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors['surface']))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors['text']))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors['text']))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors['surface']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors['text']))
        palette.setColor(QPalette.ColorRole.BrightText, QColor('#FF0000'))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor('#FFFFFF'))

        return palette

theme = Theme()
