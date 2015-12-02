#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='zcash-scale-calc',
    description='Back-of-the-scripted-envelope calculations for zcash scale parameters.',
    version='0.1.dev0',
    author='Nathan Wilcox',
    author_email='nejucomo@gmail.com',
    license='GPLv3',
    url='https://github.com/Electric-Coin-Company/zcash-scale-calc',

    packages=find_packages(),

    install_requires=[
        'dimana >= 0.1.dev0',
        ],

    entry_points={
        'console_scripts': [
            'zcash-scale-calc = zcash_scale_calc.main:main',
            ],
        },
    )
