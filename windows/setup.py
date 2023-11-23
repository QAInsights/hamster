import sys
from cx_Freeze import setup, Executable
from ..windows import __VERSION__

build_exe_options = {
    "include_files": [".\\img\\hamster.png",
                      "config.py",
                      "utils.py",
                      "__init__.py",
                      "hamster_app.properties",
                      ],
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Hamster",
    version=__VERSION__,
    description="Instantly Launch JMeter Test Plans 🚀",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("main.py", base=base)
    ],
)
