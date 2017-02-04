from io import BytesIO
from PIL import Image

import image_colors

test_values = [0,255]

def test_average_single_image_with_generated_images():
    for value in range(test_values[0], test_values[1], 8):
        im = Image.new("RGB", (200, 200), "rgb({0}, {0}, {0})".format(value))
        imagebytes = BytesIO()
        im.save(imagebytes, format="BMP")
        imagebytes.seek(0)  # rewind to the start
        result = image_colors.average_single_image(imagebytes, name='test')
        assert(result == ['test',value,value,value])
