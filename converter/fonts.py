import platform
import subprocess
from typing import Dict, List, Tuple

def get_system() -> str:
    return platform.system()

def detect_available_fonts() -> Dict[str, List[str]]:
    system = get_system()
    fonts = {
        'title': ['方正小标宋简体', '方正小标宋', 'SimHei', '黑体'],
        'body': ['仿宋_GB2312', '仿宋', 'FangSong', 'FangSong_GB2312'],
        'heading1': ['黑体', 'SimHei', 'Heiti'],
        'heading2': ['楷体_GB2312', '楷体', 'Kaiti', 'STKaiti', '楷体_GB18030'],
        'heading3': ['仿宋_GB2312', '仿宋', 'FangSong'],
        'heading4': ['仿宋_GB2312', '仿宋', 'FangSong'],
        'table': ['仿宋_GB2312', '仿宋', 'FangSong'],
    }

    if system == 'Linux':
        try:
            result = subprocess.run(
                ['fc-list', ':lang=zh', '-f', '%{family}\n'],
                capture_output=True, text=True, timeout=5
            )
            available = set()
            for line in result.stdout.split('\n'):
                for families in line.split(','):
                    available.add(families.strip())

            for category in fonts:
                fonts[category] = [f for f in fonts[category] if f in available] or fonts[category]
        except Exception:
            pass
    elif system == 'Darwin':
        font_map = {
            'title': ['方正小标宋简体', 'STHeiti'],
            'body': ['仿宋', 'STSong'],
            'heading1': ['STHeiti', '黑体'],
            'heading2': ['楷体', 'STKaiti'],
            'heading3': ['仿宋', 'STSong'],
            'heading4': ['仿宋', 'STSong'],
            'table': ['仿宋', 'STSong'],
        }
        for k, v in font_map.items():
            fonts[k] = v

    return fonts

def check_font_installed(font_name: str) -> Tuple[bool, str]:
    system = get_system()
    try:
        if system == 'Linux':
            result = subprocess.run(
                ['fc-list', ':lang=zh', '-f', '%{family}\n'],
                capture_output=True, text=True, timeout=5
            )
            available = [f.strip() for f in result.stdout.split('\n')]
            if font_name in available:
                return True, "已安装"
            return False, "未安装"
        elif system == 'Darwin':
            result = subprocess.run(
                ['system_profiler', 'SPFontsDataType'],
                capture_output=True, text=True, timeout=10
            )
            if font_name in result.stdout:
                return True, "已安装"
            return False, "未安装"
        else:
            return True, "已安装"
    except Exception as e:
        return True, f"检测失败: {str(e)}"

AVAILABLE_FONTS = detect_available_fonts()

def get_preferred_font(category: str) -> str:
    return AVAILABLE_FONTS.get(category, AVAILABLE_FONTS['body'])[0]

def get_all_font_options() -> List[str]:
    all_fonts = set()
    for fonts in AVAILABLE_FONTS.values():
        all_fonts.update(fonts)
    return sorted(list(all_fonts))

def check_all_required_fonts() -> Dict[str, Tuple[bool, str]]:
    required = [
        '方正小标宋简体', '仿宋', '仿宋_GB2312',
        '黑体', 'STHeiti', '楷体', '楷体_GB2312'
    ]
    result = {}
    for font in required:
        installed, status = check_font_installed(font)
        result[font] = (installed, status)
    return result
