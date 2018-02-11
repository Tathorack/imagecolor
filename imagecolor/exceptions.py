"""imagecolor module containing all publically raised exceptions."""

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


class ImageColorException(Exception):
    """Base Exception for all imagecolor exceptions."""

    pass


class ImageAveragingError(ImageColorException):
    """Raised when an image was unable to be averaged."""

    pass


class DirectoryAveragingError(ImageColorException):
    """Raised when an directory was unable to be averaged."""

    pass


class NoResultsError(ImageColorException):
    """Raised when a list of results is empty or invalid."""

    pass
