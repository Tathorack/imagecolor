import csv
import logging
import math
import os

from PIL import Image

"""Copyright © 2017 Rhys Hansen

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
SOFTWARE."""

logger = logging.getLogger(__name__)

def results_line(results):
    """Accepts a list of results and creates an image that is 1
    pixel tall and the length of the number of results. The
    image contains a pixel of the color of each result in the
    list of results.
    return PIL.Image.object
    """
    if len(results) == 0:
        logger.error("Nothing in results")
    else:
        im = Image.new("RGB", (len(results), 1),
            "hsl(0, 50%, 50%)")
        grid = im.load()
        for x in list(range(im.size[0])):
            grid[x,0] = (int(results[x][1]),
                      int(results[x][2]),
                      int(results[x][3]))
        return(im)

def results_rectangle(results, aspectratio=None):
    """Accepts a list of results and creates an image that is
    rectangular. The aspect ratio can be set by passing a list
    formated as [16,9] to aspectratio. The default is 3x2.
    The image contains a pixel of the color of each result in
    the list of results.
    return PIL.Image.object
    """
    if len(results) == 0:
        logger.error("Nothing in results")
    else:
        if aspectratio is None:
            aspectratio = [3,2]
        sidelength = int(math.floor(math.sqrt(len(results)
            / (aspectratio[0] * aspectratio[1]))))
        width = sidelength * aspectratio[0]
        height = sidelength * aspectratio[1]
        im = Image.new("RGB", (width, height), "hsl(0, 50%, 50%)")
        grid = im.load()
        c = 0
        for y in list(range(im.size[1])):
            for x in list(range(im.size[0])):
                grid[x, y] = (int(results[c][1]),
                          int(results[c][2]),
                          int(results[c][3]))
                c += 1
        return(im)

def results_save_csv(results, csv_out):
    """Accepts the path to a new csv file and a list containing
    results.Writes the current results to a csv file which can
    be re-loaded again by using csv_to_results. The csv created
    is formatted as follows:
    'File or Folder', 'Red', 'Green', 'Blue'
    """
    if len(results) == 0:
        logger.error("Nothing in results")
    else:
        logger.info('Opening CSV file %s for writing', csv_out.split(os.sep)[-1])
        with open(csv_out, 'w') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(['File or Folder',
                        'Red', 'Green', 'Blue'])
            for r in results:
                csv_file.writerow(r)
            f.close()

def results_load_csv(csv_in):
    """Accepts the path to a csv file formatted as follows:
    'File or Folder', 'Red', 'Green', 'Blue' parses the file
    line by line skipping the header. Returns a list containing
    an list for each line in the csv. Does not do any input checks
    other than converting the r, g, b colums to ints.
    """
    results = []
    logger.info('Opening CSV file %s for reading', csv_in.split(os.sep)[-1])
    with open(csv_in, "rt") as f:
        csv_file = csv.reader(f, delimiter=',')
        for row in csv_file:
            if row[0] in ['File','Folder','File or Folder']:
                logger.info('Skipping header')
            else:
                try:
                    row = [row[0], int(row[1]), int(row[2]), int(row[3])]
                    results.append(row)
                except Exception:
                    logger.exception('results_load_csv Exception', exc_info=True)
    return(results)
