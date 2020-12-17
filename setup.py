#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pathlib import Path

version_path = Path(__file__).parent / "karton/asciimagic/__version__.py"
version_info = {}
exec(version_path.read_text(), version_info)

setup(
    name="karton-asciimagic",
    version=version_info["__version__"],
    description="Various encoders for ascii-encoded executables for Karton framework",
    namespace_packages=["karton"],
    packages=["karton.asciimagic"],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        'console_scripts': [
            'karton-asciimagic=karton.asciimagic:AsciiMagic.main'
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
)
