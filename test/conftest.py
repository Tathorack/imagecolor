#stdlib
import os
import tempfile
#installed
from PIL import Image
import pytest

@pytest.fixture(scope="module")
def tresults():
    results = [{'name':'test.{}'.format(r), 'green':r, 'blue':r, 'red':r} for r in range(0,255)]
    return(results)

@pytest.fixture(scope="module")
def tcsv():
    t_file = tempfile.NamedTemporaryFile(suffix='.csv')
    return(t_file)

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
