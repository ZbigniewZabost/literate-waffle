from distutils.core import setup

setup(
    name='Literate Waffle',
    version='0.1',
    license='Apache License Version 2.0',
    long_description=open('README.md').read(),
    author='zbigniewz',
    url='https://github.com/zbigniewz/literate-waffle',
    requires=['elasticsearch'],
    packages=['indexer']
)
