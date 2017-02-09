#!/usr/bin/env python3
#coding=UTF-8
from .average import average
from .average import average_images
from .average import directory_average
from .average import nested_directory_average

from .loadsave import results_line
from .loadsave import results_rectangle
from .loadsave import results_save_csv
from .loadsave import results_load_csv

major_version = 1
minor_version = 1
build_version = 1

__author__ = 'Rhys Hansen'
__copyright__ = "Copyright 2017, Rhys Hansen"
__license__ = "MIT"
__version__ = '{0}.{1}.{2}'.format(major_version, minor_version, build_version)
