import os
import traceback
from datetime import datetime
from pathlib import Path
from converter import config # Import config

class Logger:
    def __init__(self):
        self.desktop = Path.home() / "Desktop"
        self.log_file = self._get_log_file_path()
        # Only ensure log file if logging is enabled
        if config.get_enable_desktop_logging():
            self._ensure_log_file()

    def _get_log_file_path(self):
        date_str = datetime.now().strftime("%Y%m%d")
        return self.desktop / f"md2gbt9704_{date_str}.log"

    def _ensure_log_file(self):
        log_path = self._get_log_file_path()
        if not log_path.exists():
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(f"# md2gbt9704 日志文件\n# 创建时间: {self._now()}\n\n")

    def _now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _format_msg(self, level, msg):
        return f"[{self._now()}] [{level}] {msg}\n"

    def _write(self, content):
        # Only write to file if desktop logging is enabled
        if not config.get_enable_desktop_logging():
            return
        try:
            log_path = self._get_log_file_path()
            self._ensure_log_file()
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            pass

    def info(self, msg):
        content = self._format_msg("INFO", msg)
        self._write(content)
        print(content.strip())

    def debug(self, msg):
        content = self._format_msg("DEBUG", msg)
        self._write(content)
        print(content.strip())

    def warning(self, msg):
        content = self._format_msg("WARNING", msg)
        self._write(content)
        print(content.strip())

    def error(self, msg, exc_info=None):
        if exc_info:
            tb = ''.join(traceback.format_exception(*exc_info))
            content = f"[{self._now()}] [ERROR] {msg}\n{tb}\n"
        else:
            content = self._format_msg("ERROR", msg)
        self._write(content)
        print(content.strip())

    def log_operation(self, operation, details=""):
        msg = f"操作: {operation}"
        if details:
            msg += f" | 详情: {details}"
        self.info(msg)


logger = Logger()
