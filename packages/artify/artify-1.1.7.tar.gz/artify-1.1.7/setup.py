import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="artify",
    version="1.1.7",
    description="Upload to Nexus, Upload files to hooks, Modify version number, Sync to GitLab type repository",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/stewiejnr",
    author="Stewartium",
    author_email="stewartium1@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=["artify"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "artify-man=artify.__main__:main",
        ]
    },
)
