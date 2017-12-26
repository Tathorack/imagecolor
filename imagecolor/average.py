#!/usr/bin/env python3
# coding=UTF-8

import imghdr
import logging
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


def average(image, name=None, downsample=True,
            max_size=100, alpha_threshold=None):
    """Average a single image.

    Averages a single image from a file or file-like object.

    Parameters
    ----------
        image : str
            A filename, pathlib.Path object or a file object.
        name : str, optional
            auto generated from path unless set.
        downsample : bool, optional
            if downsampling is enabled to speed up iteration.
        max_size : int, optional
            max length of longest side if downsample == True.
        alpha_threshold : int, optional
            level at which transparent pixels are excluded.
    Returns
    -------
        dict
            A dictionary with the following keys: name, red, green, blue.
            If the image was unable to be averaged None.
    """
    logger.debug("average called")
    if alpha_threshold is None:
        alpha_threshold = 245
    if name is None:
        name = image.split(os.sep)[-1]
    logger.debug('Image name: %s', name)
    try:
        im = Image.open(image)
        logger.debug('Image opened. Dimensions %d x %d',
                     im.size[0], im.size[1])
        if ((im.size[0] > max_size or im.size[1] > max_size)
                and downsample is True):
            im.thumbnail((max_size, max_size))
            logger.debug('Image resized to %d x %d', im.size[0], im.size[1])
        grid = im.load()
        pixelcount, r_total, g_total, b_total = 0, 0, 0, 0
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                currentpx = grid[x, y]
                try:
                    """this try-except checks to see if pixels have
                    transparency and excludes them if they are greater
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
        logger.debug('average result: Name=%s, R=%d, G=%d, B=%d',
                     name, r_avg, g_avg, b_avg)
        return({'name': name, 'red': r_avg, 'green': g_avg, 'blue': b_avg})
    except IOError as exc:
        logger.warning('Exception %s', exc)
        logger.debug('average Traceback', exc_info=True)
    else:
        return None


def average_images(dir_in):
    """Average all images in a directory.

    Accepts the path to a directory averages each individual
    image and returns a list with an entry for each image
    successfully averaged.

    Parameters
    ----------
        dir_in : str
            path to directory
    Returns
    -------
        list
            For each image averaged returns a list of dictionaries
            each with the following keys: name, red, green, blue.
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
        if imghdr.what(filepath) in ['jpeg', 'png']:
            images.append(filepath)
    with Pool(cpus) as p:
        results = (p.map(average, images))
    return(results)


def directory_average(dir_in, name=None):
    """Average all images in a directory into a single average.

    Averages the images in the directory into a directory average.

    Parameters
    ----------
        dir_in : str
            path to directory
        name : str, optional
            auto generated from path unless set
    Returns
    -------
        dict
            A dictionary with the following keys: name, red, green, blue.
            If the image was unable to be averaged None.
    """
    try:
        cpus = cpu_count()
        logger.debug('Number of CPUs detected. Setting to %d', cpus)
    except(NotImplementedError):
        cpus = 4
        logger.warning('Number of CPUs not found. Setting default to %s', cpus)
    filepaths = []
    imagecount, r_total, g_total, b_total = 0, 0, 0, 0
    if name is None:
        dir_name = os.path.normpath(dir_in)
        dir_name = dir_name.split(os.sep)
    for filename in os.listdir(dir_in):
        filepath = os.path.join(dir_in, filename)
        try:
            if imghdr.what(filepath) in ['jpeg', 'png']:
                filepaths.append(filepath)
        except(IsADirectoryError):
            logger.debug('Directory %s found, Skipping', filename)
            pass
    with Pool(cpus) as p:
        results = (p.map(average, filepaths))
    for result in results:
        try:
            r_total += result['red']
            b_total += result['green']
            g_total += result['blue']
            imagecount += 1
        except TypeError:
            logger.debug('Result not vaild. Skipping', exc_info=True)
            pass
        except AttributeError:
            logger.debug('Result not vaild. Skipping', exc_info=True)
            pass
    if imagecount > 0:
        r_avg = int(r_total / imagecount)
        g_avg = int(g_total / imagecount)
        b_avg = int(b_total / imagecount)
        return({'name': dir_name[-1], 'red': r_avg,
                'green': g_avg, 'blue': b_avg})
    else:
        logger.warning("No images in %s directory successfully averaged. "
                       "Returning None", dir_name[-1])
        return(None)


def nested_directory_average(root_dir):
    """Recursive directory average.

    Accepts the path to a directory and walks all the enclosed
    directories calling average_directory for each one that
    contains images.

    Parameters
    ----------
        dir_in : str
            path to directory
    Returns
    -------
        list
            For each directory averaged returns a list of dictionaries
            each with the following keys: name, red, green, blue.
    """
    filtered_dirs = []
    results = []
    sub_dirs = [d[0] for d in os.walk(root_dir)]
    for current_dir in sub_dirs:
        for current_file in os.listdir(current_dir):
            filepath = os.path.join(current_dir, current_file)
            try:
                if imghdr.what(filepath) in ['jpeg', 'png']:
                    filtered_dirs.append(current_dir)
                    logger.debug('Image found in directory %s. '
                                 'Appending to filtered directories',
                                 current_dir.split(os.sep)[-1])
                    break
            except(IsADirectoryError):
                pass
    for dir_path in filtered_dirs:
        result = directory_average(dir_path)
        try:
            if result is not None:
                results.append(result)
        except TypeError:
            pass
    return(results)
