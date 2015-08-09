#!/usr/bin/env python

import sys
import os
sys.path.insert(0, os.path.abspath('lib'))

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

__author__ = 'weldpua2008@gmail.com'

install_requires = ['pysphere']
if sys.version_info[:2] < (2, 7):
    install_requires.append('argparse')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='snapshot_tools',
    version='0.1',
    author='Valeriy Solovyov',
    author_email='weldpua2008@gmail.com',
    url='https://github.com/weldpua2008/snapshot_tools',
    license='GPL2',
    description='snapshot_tools is little script to manage snapshots on VMware ESX/ESXi'
                'You can create/list/delete snapshots.',
    # What does your project relate to?
    keywords='esxi vmware snapshot',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    #packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    package_dir={'': 'lib'},
    packages=find_packages('lib'),


    install_requires=install_requires,
    cmdclass={'test': PyTest},
    tests_require=['coverage', 'pytest', 'pysphere'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development',
        'Topic :: Utilities',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'esxsnapshot=esxsnapshotbin:run',
        ],
    },
    zip_safe = False,
)
