"""imagecolor initialization."""

__all__ = [
    "core_average",
    "file_average",
    "directory_average",
    "single_directory_average",
    "nested_directory_average",
    "results_line",
    "results_rectangle",
    "results_save_csv",
    "results_load_csv"]

from .average import core_average, file_average, directory_average
from .average import single_directory_average, nested_directory_average

from .loadsave import results_line, results_rectangle
from .loadsave import results_save_csv, results_load_csv


__author__ = 'Rhys Hansen'
__copyright__ = "Copyright 2017, Rhys Hansen"
__license__ = "MIT"
__version__ = '2.0.0rc1'
