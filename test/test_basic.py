#!/usr/bin/env python3
#coding=UTF-8
from io import BytesIO
import os
import logging
import sys
import tempfile
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

def test_average_from_tempfiles(tfile):
    result = ic.average(tfile.name)
    print(result)
    value = int(os.path.splitext(os.path.splitext(result.get('name'))[0])[0])
    assert result.get('red') == value
    assert result.get('green') == value
    assert result.get('blue') == value

def test_average_images_from_tempfiles(tdirectory):
    result = ic.average_images(tdirectory.name)
    print(result)
    for r in result:
        value = int(os.path.splitext(os.path.splitext(r.get('name'))[0])[0])
        assert r.get('red') == value
        assert r.get('green') == value
        assert r.get('blue') == value

def test_directory_average_from_tempfiles(tdirectory):
    result = ic.directory_average(tdirectory.name)
    print(result)
    value = int(os.path.splitext(os.path.splitext(result.get('name'))[0])[0])
    assert result.get('red') == value
    assert result.get('green') == value
    assert result.get('blue') == value

def test_nested_directory_average_from_tempfiles(tdirectories):
    result = ic.nested_directory_average(tdirectories.name)
    print(result)
    for r in result:
        print(r)
        value = int(os.path.splitext(os.path.splitext(r.get('name'))[0])[0])
        assert r.get('red') == value
        assert r.get('green') == value
        assert r.get('blue') == value

def test_results_line_from_tempresults(tresults):
    imagebytes = BytesIO()
    line = ic.results_line(tresults)
    assert line.size[0] == len(tresults)
    imagebytes = BytesIO()
    line.save(imagebytes, format="png")
    imagebytes.seek(0)
    result = ic.average(imagebytes, name='test')
    assert result.get('red') == 127
    assert result.get('green') == 127
    assert result.get('blue') == 127

def test_results_rectangle_from_tempresults(tresults):
    imagebytes = BytesIO()
    line = ic.results_rectangle(tresults)
    imagebytes = BytesIO()
    line.save(imagebytes, format="png")
    imagebytes.seek(0)
    result = ic.average(imagebytes, name='test')
    assert result.get('red') in range(0,255)
    assert result.get('green') in range(0,255)
    assert result.get('blue') in range(0,255)

def test_csv_save_and_load_from_tempfiles(tresults,tcsv):
    ic.results_save_csv(tresults, tcsv.name)
    results = ic.results_load_csv(tcsv.name)
    print(results)
    assert tresults == results
