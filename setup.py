#!/usr/bin/env python

from distutils.core import setup

requirements = []

dev_requirements = ["black~=22.1.0", "flake8~=4.0.1", "pytest~=6.2.5", "pytest-mock~=3.6.1"]

setup(
    name="tiny-web-async-framework",
    version="0.1",
    description="Web server created for educational purposes",
    author="Lukasz Olender",
    author_email="olender.lukasz96@gmail.com",
    url="https://github.com/KsaneK/tiny-web-async-framework",
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    packages=["tinyweb"],
)
