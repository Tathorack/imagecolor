"""Module containing basic tests for imagecolor."""
# pylint: disable=C0103
from io import BytesIO
import os
import imghdr
from PIL import Image
import pytest
import imagecolor


def get_value_from_temp_name(name):
    """Get the value imbedded in the prefix of a temp file or directory."""
    return int(os.path.splitext(os.path.splitext(name)[0])[0])


def test_core_average_values(test_image_creator):
    """Test core_average with values of 0, 127, 255."""
    values = (0, 127, 255)
    for value in values:
        test_file = test_image_creator(value)
        result = imagecolor.core_average(test_file.name)
        assert result['red'] == value
        assert result['green'] == value
        assert result['blue'] == value


def test_file_average_values(test_image_creator):
    """Test file_average with values of 0, 127, 255."""
    values = (0, 127, 255)
    for value in values:
        test_file = test_image_creator(value)
        result = imagecolor.file_average(test_file.name)
        assert result['name'] == test_file.name.split(os.sep)[-1]
        assert result['red'] == value
        assert result['green'] == value
        assert result['blue'] == value


def test_directory_average_tempdir(test_directory_creator):
    """Test directory_average with three images."""
    values = (0, 127, 255)
    test_directory = test_directory_creator(values)
    results = imagecolor.directory_average(test_directory.name)
    for result in results:
        value = get_value_from_temp_name(result['name'])
        assert result['name'] == '{}.png'.format(value)
        assert result['red'] == value
        assert result['green'] == value
        assert result['blue'] == value


def test_single_directory_average_tempdir(test_directory_creator):
    """Test single_directory_average with three images."""
    values = (0, 127, 255)
    test_directory = test_directory_creator(values)
    result = imagecolor.single_directory_average(test_directory.name)
    value = sum(values) // len(values)
    assert result['name'] == test_directory.name.split(os.sep)[-1]
    assert result['red'] == value
    assert result['green'] == value
    assert result['blue'] == value


def test_nested_directory_average_tempdir(test_nested_directories_creator):
    """Test directory_average with three directories."""
    pytest.skip("Issue with directories after upgrading dependencies.")
    values = (0, 127, 255)
    test_directory = test_nested_directories_creator(values)
    print(test_directory.name)
    print(os.path.exists(test_directory.name))
    results = imagecolor.nested_directory_average(test_directory.name)
    for result in results:
        value = get_value_from_temp_name(result['name'])
        assert result['name'].split('.')[0] == str(value)
        assert result['red'] == value
        assert result['green'] == value
        assert result['blue'] == value


def test_results_line_tempresults(test_results_creator):
    """Test results_line."""
    values = [x for x in range(0, 255)]
    test_results = test_results_creator(values)
    imagebytes = BytesIO()
    line = imagecolor.results_line(test_results)
    assert isinstance(line, Image.Image)
    assert line.size[0] == len(test_results)
    assert line.size[1] == 1
    imagebytes = BytesIO()
    line.save(imagebytes, format="png")
    imagebytes.seek(0)
    assert imghdr.what(imagebytes) == 'png'
    imagebytes.seek(0)
    result = imagecolor.file_average(imagebytes, name='test', downsample=False)
    value = sum(values) // len(values)
    assert result['red'] == value
    assert result['green'] == value
    assert result['blue'] == value


def test_results_rectangle_tempresults(test_results_creator):
    """Test results_rectangle."""
    values = [x for x in range(0, 150)]
    test_results = test_results_creator(values)
    imagebytes = BytesIO()
    line = imagecolor.results_rectangle(test_results)
    assert isinstance(line, Image.Image)
    imagebytes = BytesIO()
    line.save(imagebytes, format="png")
    imagebytes.seek(0)
    assert imghdr.what(imagebytes) == 'png'
    imagebytes.seek(0)
    result = imagecolor.file_average(imagebytes, name='test')
    value = sum(values) // len(values)
    assert result['red'] == value
    assert result['green'] == value
    assert result['blue'] == value


def test_results_square_tempresults(test_results_creator):
    """Test results_rectangle as a square."""
    values = [x for x in range(0, 256)]
    test_results = test_results_creator(values)
    imagebytes = BytesIO()
    line = imagecolor.results_rectangle(test_results, aspectratio=(1, 1))
    assert isinstance(line, Image.Image)
    imagebytes = BytesIO()
    line.save(imagebytes, format="png")
    imagebytes.seek(0)
    assert imghdr.what(imagebytes) == 'png'
    imagebytes.seek(0)
    result = imagecolor.file_average(imagebytes, name='test')
    value = sum(values) // len(values)
    assert result['red'] == value
    assert result['green'] == value
    assert result['blue'] == value


def test_csv_save_and_load_from_tempfile(test_results_creator, test_csv):
    """Test results_save_csv and results_load_csv."""
    values = range(0, 255)
    test_results = test_results_creator(values)
    imagecolor.results_save_csv(test_results, test_csv.name)
    results = imagecolor.results_load_csv(test_csv.name)
    assert test_results == results
