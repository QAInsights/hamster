import sys
from cx_Freeze import setup, Executable
# from windows import __VERSION__

msi_data = {

    "ProgId": [
        ("Prog.Id", None, None, "This is a description", None, None),
    ],
}

bdist_msi_options = {
    "data": msi_data,
}

build_exe_options = {
    "include_files": ["windows\\hamster.png",
                      "config.py",
                      "utils.py",
                      "hamster_app.properties",
                      ],
}
base = "Win32GUI" if sys.platform == "win32" else None

executables = [
       Executable(
            "main.py",
            copyright="Copyright (C) 2023 cx_Freeze",
            base=base,
            shortcut_name="Hamster",
        ),
    ]

setup(
    name="Hamster",
    version="0.0.1",
    description="Instantly Launch JMeter Test Plans 🚀",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
    packages=["windows"]
)
