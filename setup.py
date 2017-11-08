from setuptools import setup, find_packages

from codecs import open
from os import path

ROOT = path.abspath(path.dirname(__file__))

with open(path.join(ROOT, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='balrog-add-xpi-to-rule',
    version='0.1.0',
    description='Tool for adding an XPI file to a Balrog rule.',
    long_description=long_description,
    url='https://github.com/Osmose/balrog-add-xpi-to-rule',
    author='Osmose (Michael Kelly)',
    author_email='me@mkelly.me',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['click==6.7'],
    entry_points={
        'console_scripts': [
            'balrog-add-xpi-to-rule=balrog_add_xpi_to_rule:main',
        ],
    },
)
