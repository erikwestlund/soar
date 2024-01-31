from setuptools import setup

setup(
    name="soar",
    version="0.1.0",
    py_modules=["soar"],
    install_requires=["black", "Click", "keyring", "pyyaml", "rpy2"],
    entry_points={
        "console_scripts": [
            "soar = soar:cli",
        ],
    },
)
