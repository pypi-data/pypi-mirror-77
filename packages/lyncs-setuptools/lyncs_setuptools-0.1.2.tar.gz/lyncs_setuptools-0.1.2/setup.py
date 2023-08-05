from lyncs_setuptools import setup

setup(
    "lyncs_setuptools",
    entry_points={
        "console_scripts": ["lyncs_setuptools = lyncs_setuptools:print_keys"]
    },
    data_files=[("test", ["test/CMakeLists.txt"])],
    keywords=["Lyncs", "setuptools", "cmake",],
)
