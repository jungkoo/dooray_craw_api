# -*- coding: utf-8 -*-
# https://www.python.org/dev/peps/pep-0263/

from setuptools import setup, find_packages
import logging

logger = logging.getLogger(__name__)

doc = [
    'sphinx>=1.2.3',
    'sphinx-argparse>=0.1.13',
    'sphinx-rtd-theme>=0.1.6',
    'Sphinx-PyPI-upload>=0.2.1'
]

devel = [
]

devel_all = (devel)

setup(
    name='dooray-craw-api',
    description='dooray web craw api',
    license='Apache License 2.0',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'typing_extensions',
        'selenium>=3.131.0',
        'tinydb',
    ],
    setup_requires=[
        'docutils>=0.14, <1.0',
    ],
    extras_require={
        'all': devel_all,
        'devel': devel_all,
        'doc': doc,
    },
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3.8',
    ],
    author='deajang',
    author_email='deajang@gmail.com',
)

