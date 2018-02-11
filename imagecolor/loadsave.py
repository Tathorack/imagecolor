"""imagecolor functions for loading and saving results."""
import csv
import logging
from math import floor, sqrt
import os

from PIL import Image

from .exceptions import NoResultsError

"""Copyright © 2017-2018 Rhys Hansen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""  # pylint: disable=W0105

LOGGER = logging.getLogger(__name__)


def results_line(results):
    """Create a line of pixels from a list of results.

    Accepts a list of results and creates an image that is 1
    pixel tall and the length of the number of results. The
    image contains a pixel of the color of each result in the
    list of results.

    Parameters
    ----------
        results : list
            a list of imagecolor results
    Returns
    -------
        PIL.Image.object
            linear image containing the results

    """
    if not results:
        raise NoResultsError("No results to export!")
    image = Image.new("RGB", (len(results), 1), "hsl(0, 50%, 50%)")
    grid = image.load()
    for x in range(image.size[0]):  # pylint: disable=C0103
        grid[x, 0] = (int(results[x]['red']),
                      int(results[x]['green']),
                      int(results[x]['blue']))
    return image


def results_rectangle(results, aspectratio=(3, 2)):
    """Create a rectangle of pixels from a list of results.

    Accepts a list of results and creates an image that is
    rectangular. The aspect ratio can be set by passing a list
    formated as [16,9] to aspectratio. The default is 3x2.
    The image contains a pixel of the color of each result in
    the list of results.

    Parameters
    ----------
        results : list
            a list of imagecolor results.
        aspectratio : tuple of int
            the aspect ratio of the image being created. Format (3, 2)
    Returns
    -------
        PIL.Image.object
            rectangular image containing the results.

    """
    if not results:
        raise NoResultsError("No results to export!")
    sidelength = int(floor(sqrt(
        len(results) / (aspectratio[0] * aspectratio[1]))))
    width = sidelength * aspectratio[0]
    height = sidelength * aspectratio[1]
    image = Image.new("RGB", (width, height), "hsl(0, 50%, 50%)")
    grid = image.load()
    count = 0
    for y in range(image.size[1]):  # pylint: disable=C0103
        for x in range(image.size[0]):  # pylint: disable=C0103
            grid[x, y] = (int(results[count]['red']),
                          int(results[count]['green']),
                          int(results[count]['blue']))
            count += 1
    return image


def results_save_csv(results, path):
    """Create a csv file from a list of results.

    Accepts the path to a new csv file and a list containing
    results.Writes the current results to a csv file which can
    be re-loaded again by using csv_to_results. The csv created
    is formatted as follows:
    'File or Folder', 'Red', 'Green', 'Blue'

    Parameters
    ----------
        results : list
            a list of imagecolor results.
        path : str
            the path to the file to be created.

    """
    if not results:
        raise NoResultsError("No results to export!")
    LOGGER.info('Opening CSV file %s for writing', path.split(os.sep)[-1])
    with open(path, 'w') as fp:  # pylint: disable=C0103
        csv_file = csv.writer(fp)
        csv_file.writerow(['File or Folder', 'Red', 'Green', 'Blue'])
        for row in results:
            line = [row['name'], row['red'], row['green'], row['blue']]
            csv_file.writerow(line)


def results_load_csv(path):
    """Create a list of results from a csv file.

    Accepts the path to a csv file formatted as follows:
    'File or Folder', 'Red', 'Green', 'Blue' parses the file
    line by line skipping the header. Returns a list containing
    an list for each line in the csv. Does not do any input checks
    other than converting the r, g, b colums to ints.

    Parameters
    ----------
        path : str
            the path to the file to be loaded.
    Returns
    -------
        list
            a list of imagecolor results.

    """
    results = []
    LOGGER.info('Opening CSV file %s for reading', path.split(os.sep)[-1])
    with open(path, "rt") as fp:  # pylint: disable=C0103
        csv_file = csv.reader(fp, delimiter=',')
        for row in csv_file:
            if row[0] in ['File', 'Folder', 'File or Folder']:
                LOGGER.info('Skipping header')
            else:
                try:
                    dict_line = {'name': row[0],
                                 'red': int(row[1]),
                                 'green': int(row[2]),
                                 'blue': int(row[3])}
                    results.append(dict_line)
                except (ValueError, TypeError):
                    LOGGER.exception('results_load_csv Exception',
                                     exc_info=True)
    if results:
        return results
    raise NoResultsError("No results loaded!")
