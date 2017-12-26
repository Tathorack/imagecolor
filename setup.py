#!/usr/bin/env python3
# coding=UTF-8
import re
import os
from setuptools import setup
import codecs

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='imagecolor',
      version=find_version("imagecolor", "__init__.py"),
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
      setup_requires=[
          'pytest-runner',
        ],
      tests_require=[
        'pytest',
        ],
      include_package_data=True,
      zip_safe=False)
