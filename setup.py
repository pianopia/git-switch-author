from setuptools import setup

setup(
    name="GitSwitchAuther",
    version="0.1.0",
    install_requires=["argparse"],
    entry_points={
        "console_scripts":[
            "gsa=main:main"
        ]
    }
)
