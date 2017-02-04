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

def average_single_image(img, name=None, alpha_threshold=None):
    """Accepts an file path to an image and attempts to open it
    and average the image. Sucess returns in a list with the
    ["file name",r,g,b] values. Falure returns None.
    For the sake of speed the the image will be downsampled to
    100x100 pixels before looping over each pixel.
    """
    logger.debug("average_single_image called")
    if alpha_threshold is None:
        alpha_threshold = 250
    if name is None:
        name = img.split(os.sep)[-1]
    logger.debug('Image name: %s', name)
    try:
        im = Image.open(img)
        logger.debug('Image opened. Dementions %d x %d', im.size[0], im.size[1])
        if im.size[0] > 300 or im.size[1] > 300:
            im = im.resize((100, 100))
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
                    """ this try-except checks to see if pixels have
                    transperency and excludes them if they are greater
                    than the alpha_threshold (default=225).
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
        logger.info('average_single_image result: Name=%s, R=%d, G=%d, B=%d')
        return [name, r_avg, g_avg, b_avg]
    except Exception:
        logger.exception('average_single_image Exception', exc_info=True)
    else:
        return None

def average_directory(dir_in):
    """Accepts the path to a directory and then averages the
    images in the directory and then averages all the indivual
    image averages into a directory average. Returns a list
    containing ["directory name",r,g,b] if there are images in
    the directory that were sucussfully averaged.
    Falure returns None
    """
    try:
        cpus = cpu_count()
        logger.info('Number of CPUs detected. Setting to %d', cpus)
    except(NotImplementedError):
        cpus = 4
        logger.warning('Number of CPUs not found. Setting default to %s', cpus)
    filepaths = []
    r_total = 0
    b_total = 0
    g_total = 0
    imagecount = 0
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
    logger.info('Opening CSV file %s for reading', csv_in.split(os.sep))
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
    contains images. Returns a list with the results of with an
    entry for each directory that was averaged.
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
                        current_dir.split(os.sep))
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
    """
    try:
        cpus = cpu_count()
        logger.info('Number of CPUs detected. Setting to %d', cpus)
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
    list of results. Returns a PIL Image object that can then
    be further manipulated or saved as desired.
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
    the list of results. Returns a PIL Image object that can
    then be further manipulated or saved as desired.
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
    logger.info('Opening CSV file %s for writing', csv_out.split(os.sep))
    else:
        with open(csv_out, 'w') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(['File or Folder',
                        'Red', 'Green', 'Blue'])
            for r in results:
                csv_file.writerow(r)
            f.close()
