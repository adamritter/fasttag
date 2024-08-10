from setuptools import setup, Extension

module = Extension('fasttag', sources=['fasttag/fasttag.c'])

setup(
    name='fasttag',
    version='1.0',
    description='A simple example module written in C.',
    ext_modules=[module],
)
