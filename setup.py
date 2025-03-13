from setuptools import setup
import os

def post_install():
    """Check if ascii-image-converter is installed, if not, install it."""
    if os.system("which ascii-image-converter > /dev/null 2>&1") != 0:
        print("Installing ascii-image-converter...")
        os.system("sudo apt install -y ascii-image-converter")

setup(
    name="tuskytux",
    version="0.1",
    packages=["src"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "tuskytux=src.main:main",
        ],
    },
)

# Run post-install script
post_install()
