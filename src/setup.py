#!/usr/bin/env python3

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import flasktex

setup(
        name = "flasktex",
        version = flasktex.__version__,
        packages = find_packages(),
        install_requires = ['flask'],
        author = "Boyuan Yang",
        author_email = "073plan@gmail.com",
        description = "LaTeX building with flask",
        license = "BSD-3",
        keywords = "latex tex flask",
        url = "https://github.com/hosiet/flasktex",
        entry_points = {
            'console_scripts': [
                'flasktexd = flasktex.flasktexd:daemon_startup',
            ]
        },
)
