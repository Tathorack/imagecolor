========================================
imagecolor - Extract colors from images
========================================

|python| |pypi| |commit| |travis| |docs| |license|

.. |python| image:: https://img.shields.io/pypi/pyversions/imagecolor.svg
   :target: https://pypi.python.org/pypi/imagecolor
.. |pypi| image:: https://img.shields.io/pypi/v/imagecolor.svg
   :target: https://pypi.python.org/pypi/imagecolor
.. |commit| image:: https://img.shields.io/github/last-commit/tathorack/imagecolor.svg
   :target: https://github.com/Tathorack/imagecolor
.. |travis| image:: https://travis-ci.org/Tathorack/imagecolor.svg?branch=master
   :target: https://travis-ci.org/Tathorack/imagecolor
   :alt: Build Status
.. |docs| image:: https://readthedocs.org/projects/imagecolor/badge/?version=latest
   :target: http://imagecolor.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |license| image:: https://img.shields.io/pypi/l/imagecolor.svg
   :target: https://github.com/Tathorack/imagecolor/blob/master/LICENSE.rst

imagecolor is a python module for averaging images using pillow_. To speed up processing of multiple images it uses concurrent.futures_ to bipass the GIL by spawning worker processes.

.. _pillow: http://pillow.readthedocs.io/
.. _concurrent.futures: https://docs.python.org/3/library/concurrent.futures.html

---------------
Important notes
---------------

Warnings
--------
.. warning:: imagecolor only supports python3.6 currently.

Notes
-----
.. note:: imagecolor is only tested on macOS and Linux currently.
.. note:: imagecolor only works on 3 channel RGB images.

------------
Installation
------------

Basic Installation
------------------
Install imagecolor with :command:`pip`::

    $ pip install imagecolor

Depending on your platform you might need to install the required dependencies_ for pillow before pillow (and imagecolor) will install fully.

.. _dependencies: http://pillow.readthedocs.io/en/5.0.0/installation.html#external-libraries

--------------
Usage examples
--------------
To use imagecolor import it with ::

   import imagecolor

average an image
----------------
Average a single image file to a dict with ``red``, ``green``, & ``blue`` keys along with the file name as ``name``
::

   imagecolor.file_average(image)


average all images in a directory
---------------------------------
Averages all images in a directory to a list of dicts with ``red``, ``green``, & ``blue`` keys along with the file name as ``name``
::

   imagecolor.directory_average(image)

average a directory
-------------------
Averages all images in a directory to a dict with ``red``, ``green``, & ``blue`` keys along with the directory name as ``name``
::

   imagecolor.single_directory_average(image)

average nested directories
--------------------------
Uses ``single_directory_average`` to average the directory and all subdirectories containing images to  a list of dicts with ``red``, ``green``, & ``blue`` keys along with each directory name as ``name``
::

   imagecolor.nested_directory_average(image)


For more details read the full module reference_

.. _reference: http://imagecolor.readthedocs.io/en/read-the-docs-setup/imagecolor.html#module-imagecolor

-----------
Development
-----------

Development Installation
------------------------
image color uses pipenv_ to manage development dependencies.

.. _pipenv: http://pipenv.readthedocs.io/

Install development dependencies with :command:`pipenv`::

    $ pipenv install --dev

make commands
-------------
* ``all``: calls ``release`` and ``html``
* ``release`` checks the code with ``test`` and then calls ``source-dist`` and ``wheel-dist``
* ``source-dist`` builds a source distribution
* ``wheel-dist`` builds a wheel distribution
* ``lint`` lints imagecolor with pylint_, pycodestyle_, pydocstyle_
* ``test`` lints the code and then runs pytest_
* ``html`` builds html docs with Sphinx_
* ``clean`` cleans the build and dist directories

.. _pylint: https://pylint.readthedocs.io
.. _pycodestyle: https://pycodestyle.readthedocs.io
.. _pydocstyle: http://www.pydocstyle.org/
.. _pytest: https://pytest.readthedocs.io
.. _Sphinx: http://www.sphinx-doc.org/
