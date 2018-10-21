import os

from setuptools import setup, find_packages

# https://github.com/kennethreitz/setup.py
# Package meta-data.
AUTHOR = "Kevin Fong"
DESCRIPTION = 'Plugin manager for Taskwarrior.'
NAME = "twpm"
REQUIRES_PYTHON = '>=3.6.0'
URL = 'https://github.com/Fongshway/twpm'
VERSION = None

# What packages are required for this module to be executed?
REQUIRED = [
    "taskw",
]

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


setup(
    name=NAME,
    version=about['__version__'],
    url=URL,
    license='MIT',
    python_requires=REQUIRES_PYTHON,
    author=AUTHOR,
    install_requires=REQUIRED,
    description=DESCRIPTION,
    packages=find_packages(exclude=('tests', 'tests.*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
    entry_points={
        'console_scripts': [
            'on-add-twpm=twpm.hook_runner:on_add_runner',
            'on-modify-twpm=twpm.hook_runner:on_modify_runner',
        ],
    }
)
