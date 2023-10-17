#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "d01 <Florian Jung>"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2015-23, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.2"
__date__ = "2016-04-02"
# Created: ?

import sys
import os
from setuptools import find_packages, setup
import io

# Package meta-data.
NAME = "flotils"
DESCRIPTION = "Utility functions and classes"
URL = "https://github.com/the01/python-flotils"
EMAIL = "jungflor@gmail.com"
AUTHOR = "Florian Jung"
REQUIRES_PYTHON = ">=3.8"
VERSION = None
LICENSE = "MIT"
KEYWORDS = "flotils logging wrapper loading json baseclass"

project_slug = NAME.lower().replace("-", "_").replace(" ", "_")


def get_file(path):
    with io.open(path, "r") as f:
        return f.read()


def split_external_requirements(requirements):
    external = []
    # External dependencies
    pypi = []
    # Dependencies on pypi

    for req in requirements:
        if req.startswith("-e git+"):
            # External git link
            external.append(req.lstrip("-e git+"))
        else:
            pypi.append(req)
    return pypi, external


# What packages are required for this module to be executed?
try:
    REQUIRED, EXTERNAL = split_external_requirements(
        get_file("requirements.txt").split("\n")
    )
except Exception:
    REQUIRED = []
    EXTERNAL = []

# What packages are required to execute tests?
try:
    REQUIRED_TEST = get_file("requirements-test.txt").split("\n")
except Exception:
    REQUIRED_TEST = []

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}

if not VERSION:
    with open(os.path.join(here, "src/" + project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


history = get_file("HISTORY.rst")


if sys.argv[-1] == "build":
    quit(os.system("python setup.py clean bdist_wheel sdist --formats=gztar,zip"))
elif sys.argv[-1] == "version":
    print(about.get('__version__'))
    quit(0)
elif sys.argv[-1] == "name":
    print(NAME)
    quit(0)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description + "\n\n" + history,
    # long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    tests_require=REQUIRED_TEST,
    extras_require=EXTRAS,
    dependency_links=EXTERNAL,

    packages=[
        "flotils"
    ],
    package_dir={
        '': "src",
    },
    license=LICENSE,
    keywords=KEYWORDS,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
    ]
)
