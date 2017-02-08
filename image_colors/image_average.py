import csv
import imghdr
import logging
import math
import os
from multiprocessing import Pool, cpu_count

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

def average_single_image(image, name=None, downsample=True,
                    max_size=100, alpha_threshold=None):
    """Averages a single image from a file or file-like object.
    Arguments
    image: str
        path to image or file-like object
    name: str
        auto generated from path unless set
    downsample: bool
        if downsampling is enabled to speed up iteration
    max_size: int
        max length of longest side if downsample == True
    alpha_threshold: int
        level at which transperent pixels are excluded from average
    return ["file name",r,g,b] or None
    """
    logger.debug("average_single_image called")
    if alpha_threshold is None:
        alpha_threshold = 245
    if name is None:
        name = image.split(os.sep)[-1]
    logger.debug('Image name: %s', name)
    try:
        im = Image.open(image)
        logger.debug('Image opened. Dementions %d x %d', im.size[0], im.size[1])
        if (im.size[0] > max_size or im.size[1] > max_size) and downsample == True:
            im.thumbnail((max_size,max_size))
            logger.debug('Image resized to %d x %d', im.size[0], im.size[1])
        grid = im.load()
        pixels = []
        pixelcount = 0
        r_total = 0
        g_total = 0
        b_total = 0
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                currentpx = grid[x, y]
                try:
                    """this try-except checks to see if pixels have
                    transperency and excludes them if they are greater
                    than the alpha_threshold (default=245).
                    """
                    if currentpx[3] > alpha_threshold:
                        r_total += currentpx[0]
                        g_total += currentpx[1]
                        b_total += currentpx[2]
                        pixelcount += 1
                except IndexError:
                    r_total += currentpx[0]
                    g_total += currentpx[1]
                    b_total += currentpx[2]
                    pixelcount += 1
        r_avg = int(r_total / pixelcount)
        g_avg = int(g_total / pixelcount)
        b_avg = int(b_total / pixelcount)
        logger.debug('average_single_image result: Name=%s, R=%d, G=%d, B=%d', name, r_avg, g_avg, b_avg)
        return [name, r_avg, g_avg, b_avg]
    except Exception as e:
        logger.exception('average_single_image Exception %s', e)
        logger.debug('average_single_image Traceback', exc_info=True)
    else:
        return None

def average_directory(dir_in, name=None):
    """Averages the images in the directory into a directory average.
    Arguements
    dir_in: str
        path to directory
    name: str
        auto generated from path unless set
    return ["directory name",r,g,b] or None
    """
    try:
        cpus = cpu_count()
        logger.debug('Number of CPUs detected. Setting to %d', cpus)
    except(NotImplementedError):
        cpus = 4
        logger.warning('Number of CPUs not found. Setting default to %s', cpus)
    filepaths = []
    r_total = 0
    b_total = 0
    g_total = 0
    imagecount = 0
    if name is None:
        dir_name = os.path.normpath(dir_in)
        dir_name = dir_name.split(os.sep)
    for filename in os.listdir(dir_in):
        filepath = os.path.join(dir_in,filename)
        try:
            if imghdr.what(filepath) in ['jpeg','png']:
                filepaths.append(filepath)
        except(IsADirectoryError):
            logger.debug('Directory %s found, Skipping', filename)
            pass
    with Pool(cpus) as p:
            results = (p.map(average_single_image, filepaths))
    for result in results:
        try:
            r_total += result[1]
            b_total += result[2]
            g_total += result[3]
            imagecount += 1
        except TypeError:
            logger.debug('Result not vaild. Skipping', exc_info=True)
            pass
    if imagecount > 0:
        r_avg = int(r_total / imagecount)
        g_avg = int(g_total / imagecount)
        b_avg = int(b_total / imagecount)
        return([dir_name[-1], r_avg, g_avg, b_avg])
    else:
        logger.warning("No images in %s directory successfully averaged. Returning None", dir_name[-1])
        return(None)

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

def nested_directory_average(root_dir):
    """Accepts the path to a directory and walks all the enclosed
    directories calling average_directory for each one that
    contains images.
    Arguements
    root_dir: str
        path to directory
    return [["directory name",r,g,b],["directory name",r,g,b]]
    """
    filtered_dirs= []
    results = []
    sub_dirs = [d[0] for d in os.walk(root_dir)]
    for current_dir in sub_dirs:
        for current_file in os.listdir(current_dir):
            filepath = os.path.join(current_dir, current_file)
            try:
                if imghdr.what(filepath) in ['jpeg','png']:
                    filtered_dirs.append(current_dir)
                    logger.debug('Image found in directory %s. '
                        'Appending to filtered directories',
                        current_dir.split(os.sep)[-1])
                    break
            except(IsADirectoryError):
                pass
    for dir_path in filtered_dirs:
        result = average_directory(dir_path)
        try:
            if result != None:
                results.append(result)
        except TypeError:
            pass
    return(results)

def images_to_results(dir_in):
    """Accepts the path to a directory averages each individual
    image and returns a list with and entry for each image
    successfully averaged.
    Arguements
    dir_in: str
        path to directory
    return [["image name",r,g,b],["image name",r,g,b]]
    """
    try:
        cpus = cpu_count()
        logger.debug('Number of CPUs detected. Setting to %d', cpus)
    except(NotImplementedError):
        cpus = 4
        logger.warning('Number of CPUs not found. Setting default to %s', cpus)
    images = []
    results = []
    files = [f for f in os.listdir(dir_in)
        if os.path.isfile(os.path.join(dir_in, f))]
    for f in files:
        filepath = os.path.join(dir_in, f)
        if imghdr.what(filepath) in ['jpeg','png']:
            images.append(filepath)
    with Pool(cpus) as p:
        results = (p.map(average_single_image, images))
    return(results)

def line_from_results(results):
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

def rectangle_from_results(results, aspectratio=None):
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
