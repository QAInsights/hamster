import sys
from cx_Freeze import setup, Executable
# from windows import __VERSION__

build_exe_options = {
    "include_files": ["windows/img/hamster.png"]

}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Hamster",
    version="0.0.1",
    description="Instantly Launch JMeter Test Plans 🚀",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("windows/main.py", base=base),
        Executable("windows/config.py", base=base),
        Executable("windows/utils.py", base=base),
        Executable("windows/__init__.py", base=base),
    ],
)
