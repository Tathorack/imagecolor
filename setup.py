#!/usr/bin/env python3
#coding=UTF-8
from setuptools import setup
from codecs import open

major_version = 1
minor_version = 1
build_version = 5

version = '{0}.{1}.{2}'.format(major_version, minor_version, build_version)

setup(name='imagecolor',
    version=version,
    description='Image color extraction',
    long_description=open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Other Audience',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
    ],
    keywords='image average color',
    url='https://github.com/Tathorack/imagecolor',
    author='Rhys Hansen',
    author_email='rhyshonline@gmail.com',
    license='MIT',
    packages=['imagecolor'],
    install_requires=[
        'Pillow',
        ],
    include_package_data=True,
    zip_safe=False)
