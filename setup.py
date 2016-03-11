from distutils.core import setup

setup(
    name='Literate Waffle',
    version='0.1',
    packages=['indexer',],
    license='Apache License Version 2.0',
    long_description=open('README.md').read(), requires=['elasticsearch']
)