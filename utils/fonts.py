import platform

def get_system() -> str:
    return platform.system()

def check_font_installed(font_name: str) -> bool:
    system = get_system()
    try:
        if system == 'Linux':
            import subprocess
            result = subprocess.run(
                ['fc-list', ':lang=zh', '-f', '%{family}\n'],
                capture_output=True, text=True, timeout=5
            )
            available = [f.strip() for f in result.stdout.split('\n')]
            return font_name in available
        elif system == 'Darwin':
            import subprocess
            result = subprocess.run(
                ['system_profiler', 'SPFontsDataType'],
                capture_output=True, text=True, timeout=10
            )
            return font_name in result.stdout
        else:
            return True
    except Exception:
        return True
