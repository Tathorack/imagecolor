"""Module containing configuration for imagecolor tests with pytest."""
import os
import tempfile
from PIL import Image
import pytest


@pytest.fixture(scope="module")
def test_image_creator():
    """Create a function for generating test images."""

    def make_test_image(value, size=(200, 200)):
        """Create a test image of value."""
        test_file = tempfile.NamedTemporaryFile(suffix=".png")
        image = Image.new("RGB", size, "rgb({0}, {0}, {0})".format(value))
        image.save(test_file.name, format="png")
        return test_file

    return make_test_image


@pytest.fixture(scope="module")
def test_directory_creator():
    """Create a function for generating test directories of images."""

    def make_test_directory(values, size=(200, 200)):
        """Create a test directories with images of values."""
        test_directory = tempfile.TemporaryDirectory()
        os.chdir(test_directory.name)
        assert os.listdir(os.getcwd()) == []
        for value in values:
            image = Image.new("RGB", size, "rgb({0}, {0}, {0})".format(value))
            image.save(
                os.path.join(test_directory.name, "{}.png".format(value)), format="png"
            )
        return test_directory

    return make_test_directory


@pytest.fixture(scope="module")
def test_nested_directories_creator():
    """Create a function for generating test directories of images."""

    def make_nested_test_directories(values, size=(200, 200), image_count=3):
        """Create a test directories with images of values."""
        test_root_directory = tempfile.TemporaryDirectory()
        for value in values:
            subpath = tempfile.mkdtemp(
                prefix="{}.".format(value), dir=test_root_directory.name
            )
            for count in range(image_count):
                image = Image.new("RGB", size, "rgb({0}, {0}, {0})".format(value))
                image.save(
                    os.path.join(subpath, "{}.{}.png".format(value, count)),
                    format="png",
                )
        return test_root_directory

    return make_nested_test_directories


@pytest.fixture(scope="module")
def test_results_creator():
    def make_test_results(values):
        results = [
            {
                "name": "test.{}".format(value),
                "green": value,
                "blue": value,
                "red": value,
            }
            for value in values
        ]
        return results

    return make_test_results


@pytest.fixture(scope="module")
def test_csv():
    test_file = tempfile.NamedTemporaryFile(suffix=".csv")
    return test_file
