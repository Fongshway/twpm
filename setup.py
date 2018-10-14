from __future__ import print_function

import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='twpm',
    version="0.1.0",
    url='https://github.com/Fongshway/twpm/',
    license='MIT License',
    author='Kevin Fong',
    install_requires=[
        'taskw'
    ],
    tests_require=[
        'pytest'
    ],
    description='Plugin manager for Taskwarrior',
    packages=['twpm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
)
