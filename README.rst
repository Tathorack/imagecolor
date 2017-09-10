========================================
imagecolors - Extract colors from images
========================================

|version| |github| |python35| |license| |format|

.. |version| image:: https://img.shields.io/pypi/v/imagecolor.svg
    :target: https://pypi.python.org/pypi/imagecolor
.. |python35| image:: https://img.shields.io/badge/Python-3.5-brightgreen.svg
    :target: https://www.python.org/
.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://github.com/Tathorack/imagecolor/blob/master/LICENSE.md
.. |github| image:: https://img.shields.io/github/tag/Tathorack/imagecolor.svg
   :target: https://github.com/Tathorack/imagecolor
.. |format| image:: https://img.shields.io/pypi/format/imagecolor.svg
    :target: https://pypi.python.org/pypi/imagecolor

------------------------------------------------------------
This module uses PIL (Pillow) to extract colors from images
------------------------------------------------------------

Available functions
===================
average(image, name=None, downsample=True, max_size=100, alpha_threshold=None)
==============================================================================
Averages a single image into RGB color values. Returns a dictionary with the following keys: ``name``, ``red``, ``green``, ``blue``

* ``image`` - filename (string), pathlib.Path object or a file object. The file object must implement ``read()``, ``seek()``, and ``tell()`` methods, and be opened in binary mode.
* ``name`` -  auto generated from image path by calling ``image.split(os.sep)[-1]`` unless set.
* ``downsample`` - chooses if downsampling is enabled to speed up processing. Enabled by default.
* ``max_size`` - max length of longest side if ``downsample`` is True
* ``alpha_threshold`` - level at which transparent pixels are excluded from the average. Default is 245

average_images(dir_in)
======================
Averages each individual image in a directory and returns a list with an entry for each image successfully averaged. Returns a list containing a dictionary for each image with the following keys: ``name``, ``red``, ``green``, ``blue``

* ``dir_in`` - path to directory

directory_average(dir_in, name=None)
====================================
Averages all images in a directory to a singular RGB directory average. Returns a dictionary with the following keys: ``name``, ``red``, ``green``, ``blue``

* ``dir_in`` - path to directory
* ``name`` - auto generated from directory path by calling ``dir_in.split(os.sep)[-1]`` unless set.

nested_directory_average(root_dir)
==================================
Accepts the path to a directory and walks all the enclosed directories calling ``average_directory`` for each one that contains images. Returns a list containing a dictionary for each directory with the following keys: ``name``, ``red``, ``green``, ``blue``

* ``root_dir`` - path to starting directory

Future work
===========
* add usage examples to readme
* add information for loadsave functions to readme

Tests
=====
Testing is done with pytest_

.. _pytest: http://docs.pytest.org/en/latest/

Run with ``python3 setup.py test``
