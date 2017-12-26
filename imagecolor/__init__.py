#!/usr/bin/env python3
# coding=UTF-8

__all__ = ["average", "average_images", "directory_average", "nested_directory_average", "results_line", "results_rectangle", "results_save_csv", "results_load_csv"]

from .average import average
from .average import average_images
from .average import directory_average
from .average import nested_directory_average

from .loadsave import results_line
from .loadsave import results_rectangle
from .loadsave import results_save_csv
from .loadsave import results_load_csv

major_version = 1
minor_version = 2
build_version = 0

__author__ = 'Rhys Hansen'
__copyright__ = "Copyright 2017, Rhys Hansen"
__license__ = "MIT"
__version__ = '{0}.{1}.{2}'.format(major_version, minor_version, build_version)
