# coding=utf-8
""" Pykaf setup.py package.

    https://docs.python.org/2/distutils/index.html

"""
from setuptools import setup

setup(
    name='pynaf',
    version='2.0.2',
    author='Rodrigo Agerri',
    author_email='rodrigo.agerri@ehu.es',
    packages=['pynaf',],
    url='https://github.com/josubg/pynaf/',
    license=' Apache License 2.0 (APL 2.0)',
    description='Read and create NAF annotation Documents.',
    long_description=open('LONG.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML', 
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='NLP XML markup NAF',
    install_requires=['lxml']
)

