import sys
from cx_Freeze import setup, Executable
# from windows import __VERSION__

msi_data = {
    "ProgId": [
        ("Prog.Id", None, None, "Hamster - Instantly Launch JMeter Test Plans", "IconId", None),
    ],
    "Icon": [
        ("IconId", r'windows\\hamster.ico'),
    ],
}

bdist_msi_options = {
    "data": msi_data,
    "install_icon": r'windows\\hamster.ico',
    "initial_target_dir": r'[ProgramFilesFolder]\%s\%s' % ("QAInsights", "Hamster"),
    "summary_data": {
        "author": "QAInsights",
        "comments": "Hamster - Instantly Launch JMeter Test Plans",
        "keywords": "JMeter, Performance Testing, QAInsights, Apache JMeter, Hamster",
    },
}

build_exe_options = {
    "include_files": ["windows\\hamster.png",
                      "windows\\config.py",
                      "windows\\utils.py",
                      "windows\\hamster_app.properties",
                      "windows\\hamster.ico",
                      ],
}
base = "Win32GUI" if sys.platform == "win32" else None

executables = [
       Executable(
            "windows\\main.py",
            copyright="Copyright (C) 2023 QAInsights",
            base=base,
            shortcut_name="Hamster",
            shortcut_dir="ProgramMenuFolder",
            icon="windows\\hamster.ico",
        ),
    ]

setup(
    name="Hamster",
    version="0.0.1",
    description="Hamster - Instantly Launch JMeter Test Plans 🚀",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
    packages=["windows"]
)
