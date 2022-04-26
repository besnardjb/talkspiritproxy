import setuptools
from distutils.core import setup

setuptools.setup(
    name='talkspiritproxy',
    version='0.1',
    author='Jean-Baptiste BESNARD',
    description='A Slack notification proxy for Talkspirit.',
    entry_points = {
        'console_scripts': ['tsproxy=lib.tsproxy:cli_entry'],
    },
    packages=["lib.tsproxy"],
    install_requires=["flask"
    ],
    python_requires='>=3.5'
)