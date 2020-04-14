# coding=utf-8
""" pynaf setup.py package.

    https://docs.python.org/3/distutils/index.html

"""
from setuptools import setup

setup(
    name='pynaf',
    version='3.0.0',
    author='Rodrigo Agerri',
    author_email='rodrigo.agerri@ehu.eus',
    packages=['pynaf',],
    url='https://github.com/ixa-ehu/pynaf/',
    license=' Apache License 2.0 (APL 2.0)',
    description='Read and create NAF documents',
    long_description=open('LONG.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML', 
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='NLP XML markup NAF',
    install_requires=['lxml']
)

