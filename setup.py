from setuptools import setup, find_packages
import re

PACKAGE="cephfs_srr"
MAIN="storage_summary"

# Read version from storage-summary.py
def get_version():
    with open(f"{PACKAGE}/{MAIN}.py", "r") as f:
        match = re.search(r'APP_VERSION\s*=\s*"(.+?)"', f.read())
        if match:
            return match.group(1)
        raise RuntimeError("APP_VERSION not found in "+MAIN)

setup(
    name=PACKAGE,
    version=get_version(),
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
           f"{MAIN}={PACKAGE}.{MAIN}:main"
         ]
    },
)
