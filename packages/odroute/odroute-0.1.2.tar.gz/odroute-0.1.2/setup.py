# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

INSTALL_REQUIREMENTS = [
    'Click>=6.0,<7.0',
    'pyzmq>=16.0,<17.0',
    'click_log>=0.1.4,<=0.1.8',
    'tornado>=4.0,<5.0',
    'oyaml>=0.4',
]

setup(
    author='Jonas Ohrstrom',
    author_email='ohrstrom@gmail.com',
    url='https://github.com/digris/odr-stream-router',
    name='odroute',
    version='0.1.2',
    description='A tool to route streams from ODR-AudioEnc',
    packages=find_packages(),
    install_requires=INSTALL_REQUIREMENTS,
    entry_points='''
        [console_scripts]
        odroute=odroute:cli.odr_cli
    ''',
)
