"""imagecolor functions for averaging images."""

import logging
import os
from operator import add
import concurrent.futures

from PIL import Image

from .exceptions import ImageAveragingError, DirectoryAveragingError
from .utilities import _images_from_dir, _directories_with_images

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


def single_directory_average(path, image_formats=('jpeg', 'png')):
    """Average all images in a directory into a single average.

    Accepts the path to a directory and averages each all images together
    into a single directory average. Uses concurrent.futures to process
    images in paralell. If images fail to average successfully, the
    exceptions are caught and logged allowing other images to finish.
    By default only averages jpeg and png images.

    Parameters
    ----------
    path : str
        Path to directory.
    image_formats : touple of str, optional
        touple of image formats used by imghdr to determine what types
        of images to average. Defaults: ('jpeg', 'png')

    Returns
    -------
    dict
        A dictionary with the following keys: name, red, green, blue.

    Raises
    ------
    DirectoryAveragingError
        If the directory could not be averaged.

    """
    name = os.path.abspath(path).split(os.sep)[-1]
    results = directory_average(path, image_formats=image_formats)
    imagecount = 0
    accum = {'red': 0, 'green': 0, 'blue': 0}
    for image in results:
        accum['red'] += image['red']
        accum['green'] += image['green']
        accum['blue'] += image['blue']
        imagecount += 1
    if imagecount:
        result = {key: value // imagecount for key, value in accum.items()}
        LOGGER.debug('single_directory_average result: '
                     'Name=%s, R=%d, G=%d, B=%d', name,
                     result['red'], result['green'], result['blue'])
        return {'name': name, 'red': result['red'],
                'green': result['green'], 'blue': result['blue']}
    raise DirectoryAveragingError('Unable to average directory!')


def nested_directory_average(path, image_formats=('jpeg', 'png')):
    """Averages all subdirectories into a directory average for each directory.

    Accepts the path to a directory and walks all the enclosed
    directories calling single_directory_average for each one that
    contains images. Uses concurrent.futures to process images in paralell.
    If images fail to average successfully, the exceptions are caught and
    logged allowing other images to finish. By default only averages
    jpeg and png images.

    Parameters
    ----------
    path : str
        path to directory
    image_formats : touple of str, optional
        touple of image formats used by imghdr to determine what types
        of images to average. Defaults: ('jpeg', 'png')

    Returns
    -------
    list
        For each directory averaged, returns a list of dictionaries
        each with the following keys: name, red, green, blue.

    """
    filtered_paths = _directories_with_images(
        path, image_formats=image_formats)
    results = []
    for dpath in filtered_paths:
        try:
            results.append(single_directory_average(
                dpath, image_formats=image_formats))
        except DirectoryAveragingError as exc:
            LOGGER.warning('single_directory_average failed: %s', exc)
            LOGGER.debug('Traceback', exc_info=True)
    if results:
        return results
    raise DirectoryAveragingError('Unable to average directories')
