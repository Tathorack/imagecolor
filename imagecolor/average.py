"""imagecolor functions for averaging images."""

import logging
import os
from operator import add
import concurrent.futures

from PIL import Image

from .exceptions import ImageAveragingError, DirectoryAveragingError
from .utilities import _images_from_dir, _directories_with_images

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

LOGGER = logging.getLogger(__name__)


def core_average(image, downsample=True, max_size=100, alpha_threshold=245):
    """Average a single image.

    Averages a single image from a file or file-like object. By default
    downsamples images that are larger than 100px on the long side for speed.
    Ignores pixels that are more transperent than the alpha_threshold.

    Parameters
    ----------
        image : str
            A filename, pathlib.Path object or a file object.
        downsample : bool, optional
            if downsampling is enabled to speed up iteration.
        max_size : int, optional
            max length of longest side if downsample == True.
        alpha_threshold : int, optional
            level at which transparent pixels are excluded.
    Returns
    -------
        dict
            A dictionary with the following keys: red, green, blue.
    Raises
    ------
        IOError
            If the file cannot be found, or the image cannot be
            opened and identified.
        ImageAveragingError
            If the image could not be averaged.

    """
    LOGGER.debug("core_average called")
    try:
        image = Image.open(image)
        LOGGER.debug('Image opened. Dimensions %d x %d',
                     image.size[0], image.size[1])
        if ((image.size[0] > max_size or image.size[1] > max_size)
                and downsample is True):
            image.thumbnail((max_size, max_size))
            LOGGER.debug('Image resized to %d x %d',
                         image.size[0], image.size[1])
        # load the pixels of the image into a 2D array.
        grid = image.load()
        pixelcount = 0
        pixelaccum = [0, 0, 0]  # Accumulator list for Red, Green, Blue.
        for x in range(image.size[0]):  # pylint: disable=C0103
            for y in range(image.size[1]):  # pylint: disable=C0103
                currentpx = grid[x, y]
                try:
                    # Check the value of the alpha channel.
                    if currentpx[3] > alpha_threshold:
                        # Add pixel values if above alpha_threshold.
                        pixelaccum = list(map(add, pixelaccum, currentpx))
                        pixelcount += 1
                except IndexError:
                    # If no alpha channel add pixel values.
                    pixelaccum = list(map(add, pixelaccum, currentpx))
                    pixelcount += 1
        # Get the average of each channel
        result = [value // pixelcount for value in pixelaccum]
        LOGGER.debug('average result: R=%d, G=%d, B=%d', *result)
        return {'red': result[0], 'green': result[1], 'blue': result[2]}
    except ZeroDivisionError:  # No pixels averaged
        LOGGER.debug('Traceback', exc_info=True)
        raise ImageAveragingError(
            "No pixels averaged in image! If the image has transperency, "
            "try raising the alpha_threshold.")
    except TypeError:  # single channel image
        LOGGER.debug('Traceback', exc_info=True)
        raise ImageAveragingError("Single channel image! Try an RGB image.")


def file_average(image, name=None, downsample=True,
                 max_size=100, alpha_threshold=245):
    """Average a single image and keep track of its file name.

    Averages a single image from a file or file-like object. name is
    extracted from the filepath unless set. By default downsamples images
    that are larger than 100px on the long side for speed.
    Ignores pixels that are more transperent than the alpha_threshold.

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
    Raises
    ------
        AttributeError
            If name is not passed in and cannot be set from filepath.
        IOError
            If the file cannot be found, or the image cannot be
            opened and identified.
        ImageAveragingError
            If the image could not be averaged.

    """
    if name is None:
        name = image.split(os.sep)[-1]
    LOGGER.debug('Image name: %s', name)
    result = core_average(image, downsample=downsample,
                          max_size=max_size,
                          alpha_threshold=alpha_threshold)
    result['name'] = name
    return result


def directory_average(path, image_formats=('jpeg', 'png')):
    """Average all images in a directory.

    Accepts the path to a directory and averages each individual image.
    Uses concurrent.futures to process images in paralell. If images fail
    to average successfully, the exceptions are caught and logged allowing
    other images to finish. By default only averages jpeg and png images.

    Parameters
    ----------
        path : str
            Path to directory.
        image_formats : touple of str, optional
            touple of image formats used by imghdr to determine what types
            of images to average. Defaults: ('jpeg', 'png')
    Returns
    -------
        list
            For each image averaged, returns a list of dictionaries
            each with the following keys: name, red, green, blue.
    Raises
    ------
        ImageAveragingError
            If no images were averaged successfully.

    """
    images = _images_from_dir(path, image_formats=image_formats)
    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Create a list of futures for each image to be averaged.
        future_to_image = [executor.submit(file_average, image)
                           for image in images]
        # As the futures are completed access the results.
        for future in concurrent.futures.as_completed(future_to_image):
            try:
                data = future.result()
                LOGGER.debug('future.result: name=%s R=%d, G=%d, B=%d',
                             data['name'], data['red'],
                             data['green'], data['blue'])
                # If the result is valid append it to results.
                results.append(data)
            except ImageAveragingError as exc:
                # If file_average failed, catch exceptions and log them.
                LOGGER.warning('file_average failed: %s', exc)
                LOGGER.debug('Traceback', exc_info=True)
    if results:
        return results
    raise ImageAveragingError("No images successfully averaged!")

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
        LOGGER.debug('Number of CPUs detected. Setting to %d', cpus)
    except(NotImplementedError):
        cpus = 4
        LOGGER.warning('Number of CPUs not found. Setting default to %s', cpus)
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
            LOGGER.debug('Directory %s found, Skipping', filename)
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
            LOGGER.debug('Result not vaild. Skipping', exc_info=True)
            pass
        except AttributeError:
            LOGGER.debug('Result not vaild. Skipping', exc_info=True)
            pass
    if imagecount > 0:
        r_avg = int(r_total / imagecount)
        g_avg = int(g_total / imagecount)
        b_avg = int(b_total / imagecount)
        return({'name': dir_name[-1], 'red': r_avg,
                'green': g_avg, 'blue': b_avg})
    else:
        LOGGER.warning("No images in %s directory successfully averaged. "
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
                    LOGGER.debug('Image found in directory %s. '
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
