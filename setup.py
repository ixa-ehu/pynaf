# coding=utf-8
""" Pykaf setup.py package.

    https://docs.python.org/2/distutils/index.html

"""
from distutils.core import setup

setup(
    name='pynaf',
    version='2.0',
    author='Rodrigo Agerri',
    author_email='rodrigo.agerri@ehu.es',
    packages=['pynaf',],
    url='https://github.com/josubg/pynaf/',
    license='LICENSE',
    description='Read and create NAF annotation Documents.',
    install_requires=['lxml'],
    long_description=open('README.md').read(),
)

