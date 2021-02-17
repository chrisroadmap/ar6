import os.path

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

import versioneer

PACKAGE_NAME = "ar6"
AUTHORS = [
    ("Chris Smith", "smithc@iiasa.ac.uk"),
]
URL = "https://github.com/chrisroadmap/ar6"

DESCRIPTION = "AR6-related work"
README = "README.md"

SOURCE_DIR = "src"

REQUIREMENTS = [
    "fair==1.6.2",
    "matplotlib",
    "numpy",
    "scipy",
    "pandas",
    "wquantiles",
    "h5py",
    "netCDF4>=1.5.6",
    "tqdm",
    "xlrd",
    "statsmodels",
    "openscm-runner",
    "jupyter"
]

# no tests/docs in `src` so don't need exclude
PACKAGES = find_packages(SOURCE_DIR)
PACKAGE_DIR = {"": SOURCE_DIR}

# README #
def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name=PACKAGE_NAME,
    version=versioneer.get_version(),
    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type="text/x-rst",
    author=", ".join([author[0] for author in AUTHORS]),
    author_email=", ".join([author[1] for author in AUTHORS]),
    url=URL,
    license="3-Clause BSD License",
    classifiers=[  # full list at https://pypi.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["climate", "model"],
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    cmdclass=versioneer.get_cmdclass(),
)
