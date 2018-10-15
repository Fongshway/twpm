from setuptools import setup, find_packages

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
    packages=find_packages(exclude=('tests',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
    entry_points={
        'console_scripts': [
            'on-add-twpm=twpm.hook_runner:on_add_runner',
            'on-modify-twpm=twpm.on_modify_twpm:on_modify_runner',
        ],
    }
)
