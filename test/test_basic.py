#stdlib
from io import BytesIO
import os
import sys
#installed
from PIL import Image
import pytest
#local
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])
import imagecolor

test_values = [0,255]

def test_average_with_generated_images():
    for value in range(test_values[0], test_values[1], 8):
        im = Image.new("RGB", (200, 200), "rgb({0}, {0}, {0})".format(value))
        imagebytes = BytesIO()
        im.save(imagebytes, format="png")
        imagebytes.seek(0)  # rewind to the start
        result = imagecolor.average(imagebytes, name='test')
        assert(result == ['test',value,value,value])
