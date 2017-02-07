#stdlib
from io import BytesIO
import os
import sys
#installed
from PIL import Image
import pytest
#local
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])
import image_colors

test_values = [0,255]

def test_average_single_image_with_generated_images():
    for value in range(test_values[0], test_values[1], 8):
        im = Image.new("RGB", (200, 200), "rgb({0}, {0}, {0})".format(value))
        imagebytes = BytesIO()
        im.save(imagebytes, format="png")
        imagebytes.seek(0)  # rewind to the start
        result = image_colors.average_single_image(imagebytes, name='test')
        assert(result == ['test',value,value,value])

def test_cwd():
    location = __file__
    test_dir = os.path.split(location)[0]
    project_dir = os.path.split(test_dir)[0]
    assert location == '/Users/rhyshansen/programming/source/Python/imagecolors/test/test_basic.py'
    assert test_dir == '/Users/rhyshansen/programming/source/Python/imagecolors/test'
    assert project_dir == '/Users/rhyshansen/programming/source/Python/imagecolors'
