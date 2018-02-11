"""utility functions for imagecolor."""

import os
import imghdr


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


def _images_from_dir(path, image_formats=('jpeg', 'png')):
    """Get all images from a directory."""
    basepath = os.path.abspath(path)
    with os.scandir(basepath) as entries:
        images = [os.path.join(basepath, entry.name)
                  for entry in entries
                  if entry.is_file()
                  and imghdr.what(os.path.join(basepath, entry.name))
                  in image_formats]
    return images


def _directories_with_images(path, image_formats=('jpeg', 'png')):
    """Get all sub directories with images."""
    filtered_paths = []
    basepath = os.path.abspath(path)
    directory_paths = [dpath for dpath, dname, fname in os.walk(basepath)]
    for dpath in directory_paths:
        with os.scandir(dpath) as entries:
            for entry in entries:
                if (entry.is_file()
                        and imghdr.what(os.path.join(dpath, entry.name))
                        in image_formats):
                    filtered_paths.append(dpath)
                    break
    return filtered_paths
