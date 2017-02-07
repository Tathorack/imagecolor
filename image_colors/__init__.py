
from .image_average import average_single_image

from .image_average import images_to_results

from .image_average import average_directory
from .image_average import nested_directory_average

from .image_average import line_from_results
from .image_average import rectangle_from_results

from .image_average import results_save_csv
from .image_average import results_load_csv

major_version = 0
minor_version = 0
build_version = 2

__author__ = 'Rhys Hansen'
__copyright__ = "Copyright 2017, Rhys Hansen"
__license__ = "MIT"
__version__ = str(major_version) + '.' + str(minor_version) + '.' + str(build_version)
