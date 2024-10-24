from setuptools import setup, Extension

module = Extension('fasttag', sources=['fasttag/fasttag.c'])

setup(
    name='fasttag',
    version='0.1.6',
    description='Extremely fast HTML tag generator',
    ext_modules=[module],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Adam Ritter',
    author_email='aritter@gmail.com',
    url='https://github.com/adamritter/fasttag',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

# Release:
# python setup.py sdist bdist_wheel
# python -m twine upload dist/* --verbose
