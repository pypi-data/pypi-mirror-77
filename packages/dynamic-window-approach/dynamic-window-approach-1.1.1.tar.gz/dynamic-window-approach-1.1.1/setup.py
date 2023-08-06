#!/usr/bin/env python3

import os
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dynamic-window-approach',
    description='Dynamic Window Approach algorithm written in C with Python Bindings',
    version='1.1.1',
    author='Göktuğ Karakaşlı',
    author_email='karakasligk@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    ext_modules = cythonize([Extension("dwa", ["python/dwa.pyx"],
                                       include_dirs=[numpy.get_include(), 'src'],
                                       define_macros = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')])],
                            compiler_directives={'language_level' : "3"}),
    url='https://github.com/goktug97/DynamicWindowApproach',
    download_url=(
        'https://github.com/goktug97/DynamicWindowApproach/archive/v1.1.0.tar.gz'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        'cython',
        'numpy',
    ],
    python_requires='>=3.6',
    include_package_data=True)
