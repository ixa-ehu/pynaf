from distutils.core import setup

setup(
    name='pynaf',
    version='1.0',
    author='Rodrigo Agerri',
    author_email='rodrigo.agerri@ehu.es',
    packages=['pynaf',],
    url='https://github.com/ixa-ehu/pynaf',
    license='LICENSE',
    description='Read and create NAF annotation Documents.',
    install_requires=[],
    long_description=open('README.md').read(),
)

