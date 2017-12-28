"""utility functions for imagecolor."""

import os
import imghdr


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
