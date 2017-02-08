#stdlib
import os
import logging
# import shutil
import sys
import tempfile
import time
#installed
from PIL import Image
import pytest
#local
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])
import imagecolor as ic

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

@pytest.fixture(scope="module")
def tfile():
    value = 127
    t_file = tempfile.NamedTemporaryFile(suffix='.png', prefix='{}.'.format(value))
    im = Image.new("RGB", (200, 200), "rgb({0}, {0}, {0})".format(value))
    print(t_file.name)
    im.save(t_file.name, format="png")
    return(t_file)

@pytest.fixture(scope="module")
def tdirectory():
    t_directory = tempfile.TemporaryDirectory(prefix='{}.'.format(127))
    os.chdir(t_directory.name)
    assert os.listdir(os.getcwd()) == []
    for value in [0,127,255]:
        im = Image.new("RGB", (200, 200), "rgb({0}, {0}, {0})".format(value))
        im.save(os.path.join(t_directory.name, '{}.png'.format(value)), format="png")
    return(t_directory)

@pytest.fixture(scope="module")
def tdirectories():
    t_directory = tempfile.TemporaryDirectory(prefix='{}.'.format(127))
    for value in [0,127,255]:
        subpath = tempfile.mkdtemp(prefix='{}.'.format(value),dir=t_directory.name)
        for num in range(3):
            im = Image.new("RGB", (200, 200), "rgb({0}, {0}, {0})".format(value))
            im.save(os.path.join(subpath, '{}.{}.png'.format(value,num)), format="png")
    return(t_directory)

def test_average_from_tempfiles():
    test_f = tfile()
    result = ic.average(test_f.name)
    print(result)
    value = int(os.path.splitext(os.path.splitext(result[0])[0])[0])
    assert(result == [result[0],value,value,value])

def test_average_images_from_tempfiles():
    test_d = tdirectory()
    result = ic.average_images(test_d.name)
    print(result)
    for r in result:
        value = int(os.path.splitext(os.path.splitext(r[0])[0])[0])
        assert(r == [r[0],value,value,value])

def test_directory_average_from_tempfiles():
    test_d = tdirectory()
    result = ic.directory_average(test_d.name)
    print(result)
    value = int(os.path.splitext(os.path.splitext(result[0])[0])[0])
    assert(result == [result[0],value,value,value])

def test_nested_directory_average_from_tempfiles():
    test_nd = tdirectories()
    print(test_nd.name)
    result = ic.nested_directory_average(test_nd.name)
    print(result)
    for r in result:
        print(r)
        value = int(os.path.splitext(os.path.splitext(r[0])[0])[0])
        assert(r == [r[0],value,value,value])
