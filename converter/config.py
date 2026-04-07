import json
import platform
from pathlib import Path
from typing import Dict, Any

class Config:
    DEFAULT_CONFIG = {
        "version": "1.0",
        "margins": {
            "top": 37,
            "bottom": 35,
            "left": 27,
            "right": 27
        },
        "fonts": {
            "title": "方正小标宋简体",
            "heading1": "黑体",
            "heading2": "楷体",
            "heading3": "仿宋",
            "heading4": "仿宋",
            "body": "仿宋",
            "table": "仿宋"
        },
        "font_sizes": {
            "title": 22,
            "heading": 16,
            "body": 16,
            "table": 12
        },
        "line_spacing": 28,
        "char_indent": 32,
        "preset": "gbt9704",
        "enable_desktop_logging": False # New setting for desktop logging
    }

    PRESETS = {
        "gbt9704": {
            "name": "GB/T 9704-2012（党政机关公文格式）",
            "margins": {"top": 37, "bottom": 35, "left": 27, "right": 27},
            "font_sizes": {"title": 22, "heading": 16, "body": 16, "table": 12},
            "line_spacing": 28
        },
        "administration": {
            "name": "国家行政机关公文格式",
            "margins": {"top": 35, "bottom": 35, "left": 28, "right": 20},
            "font_sizes": {"title": 22, "heading": 16, "body": 16, "table": 12},
            "line_spacing": 28
        }
    }

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self._config = None
        self.load()

    def _get_config_dir(self) -> Path:
        if platform.system() == "Windows":
            base = Path.home() / "AppData" / "Local"
        else:
            base = Path.home() / ".config"
        return base / "md2gbt9704"

    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self._config = {**self.DEFAULT_CONFIG, **loaded}
            except Exception:
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()

    def save(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def set(self, key: str, value: Any):
        keys = key.split('.')
        target = self._config
        for i, k in enumerate(keys):
            if i == len(keys) - 1:
                target[k] = value
            else:
                if k not in target or not isinstance(target[k], dict):
                    target[k] = {}
                target = target[k]
        self.save()

    def get_margins(self) -> Dict[str, int]:
        return self._config.get("margins", self.DEFAULT_CONFIG["margins"])

    def set_margins(self, margins: Dict[str, int]):
        self._config["margins"] = margins
        self.save()

    def get_fonts(self) -> Dict[str, str]:
        return self._config.get("fonts", self.DEFAULT_CONFIG["fonts"])

    def set_fonts(self, fonts: Dict[str, str]):
        self._config["fonts"] = fonts
        self.save()

    def get_font_sizes(self) -> Dict[str, int]:
        return self._config.get("font_sizes", self.DEFAULT_CONFIG["font_sizes"])

    def set_font_sizes(self, font_sizes: Dict[str, int]):
        self._config["font_sizes"] = font_sizes
        self.save()

    def get_line_spacing(self) -> int:
        return self._config.get("line_spacing", self.DEFAULT_CONFIG["line_spacing"])

    def set_line_spacing(self, line_spacing: int):
        self._config["line_spacing"] = line_spacing
        self.save()

    def get_char_indent(self) -> int:
        return self._config.get("char_indent", self.DEFAULT_CONFIG["char_indent"])

    def set_char_indent(self, char_indent: int):
        self._config["char_indent"] = char_indent
        self.save()

    def apply_preset(self, preset_key: str):
        if preset_key in self.PRESETS:
            preset = self.PRESETS[preset_key]
            self._config["margins"] = preset["margins"]
            self._config["font_sizes"] = preset["font_sizes"]
            self._config["line_spacing"] = preset["line_spacing"]
            self._config["preset"] = preset_key
            self.save()

    def reset_to_default(self):
        self._config = self.DEFAULT_CONFIG.copy()
        self.save()

    def get_enable_desktop_logging(self) -> bool:
        return self._config.get("enable_desktop_logging", self.DEFAULT_CONFIG["enable_desktop_logging"])

    def set_enable_desktop_logging(self, enable: bool):
        self._config["enable_desktop_logging"] = enable
        self.save()

config = Config()
