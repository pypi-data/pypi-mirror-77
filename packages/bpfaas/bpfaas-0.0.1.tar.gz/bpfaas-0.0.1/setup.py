#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='bpfaas',
    version='0.0.1',
    description=(
        'bpfaas python SDK'
    ),
    long_description=open('README.rst').read(),
    author='brainpoint',
    author_email='bpoint.lee@gmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/bpfaas/sdk-python#readme',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
)