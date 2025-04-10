# setup.py
from setuptools import setup, find_packages

setup(
    name="ei_mobly",  # Name of your library
    version="0.1.0",   # Version of your library
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[
        'mobly',  # Make sure Mobly is installed as a dependency
        'snippet_uiautomator'
    ],
    description="A library for controlling system level settings on Android devices using Mobly.",
    author="Aditya Patel",
    author_email="aditya.patel@einfochips.com",
    license="MIT",
)
