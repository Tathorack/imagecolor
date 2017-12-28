"""imagecolor module containing all publically raised exceptions."""


class ImageColorException(Exception):
    """Base Exception for all imagecolor exceptions."""

    pass


class ImageAveragingError(ImageColorException):
    """Raised when an image was unable to be averaged."""

    pass


class DirectoryAveragingError(ImageColorException):
    """Raised when an directory was unable to be averaged."""

    pass
