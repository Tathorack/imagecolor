import csv
import imghdr
import math
import os
from multiprocessing import Pool, cpu_count
from PIL import Image

"""Copyright © 2017 Rhys Hansen

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
SOFTWARE."""

def average_single_image(img, name=None, alpha_threshold=None):
    """Accepts an file path to an image and attempts to open it
    and average the image. Sucess returns in a list with the
    ["file name",r,g,b] values. Falure returns None.
    For the sake of speed the the image will be downsampled to
    100x100 pixels before looping over each pixel.
    """
    if alpha_threshold is None:
        alpha_threshold = 250
    if name is None:
        name = img.split(os.sep)[-1]
    try:
        im = Image.open(img)
        if im.size[0] > 300 or im.size[1] > 300:
            im = im.resize((100, 100))
        grid = im.load()
        pixels = []
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                pixel = grid[x, y]
                pixels.append(pixel)
        r = 0
        g = 0
        b = 0
        count = 0
        for p in range(len(pixels)):
            """ this try-except checks to see if pixels have
            transperency and excludes them if they are greater
            than the alpha_threshold (default=225).
            """
            try:
                if pixels[p][3] > alpha_threshold:
                    r+=pixels[p][0]
                    g+=pixels[p][1]
                    b+=pixels[p][2]
            except:
                r+=pixels[p][0]
                g+=pixels[p][1]
                b+=pixels[p][2]
            count += 1
        r = int(r / count)
        g = int(g / count)
        b = int(b / count)
        imgavg = [name, r, g, b]
        return imgavg
    except Exception as e:
        print(e)
    else:
        return None

def average_directory(dirin):
    """Accepts the path to a directory and then averages the
    images in the directory and then averages all the indivual
    image averages into a directory average. Returns a list
    containing ["directory name",r,g,b] if there are images in
    the directory that were sucussfully averaged.
    Falure returns None
    """
    try:
        cpus = cpu_count()
    except(NotImplementedError):
        cpus = 4
    filepaths = []
    r_total = 0
    b_total = 0
    g_total = 0
    imgcount = 0
    dir_name = os.path.normpath(dirin)
    dir_name = dir_name.split(os.sep)
    for filename in os.listdir(dirin):
        filepath = os.path.join(dirin,filename)
        try:
            if imghdr.what(filepath) in ['jpeg','png']:
                filepaths.append(filepath)
        except(IsADirectoryError):
            pass
    with Pool(cpus) as p:
            results = (p.map(average_single_image, filepaths))
    try:
        for result in results:
            r_total += result[1]
            b_total += result[2]
            g_total += result[3]
            imgcount += 1
    except Exception as e:
        print(e)
    if imgcount > 0:
        r_avg = int(r_total/imgcount)
        g_avg = int(g_total/imgcount)
        b_avg = int(b_total/imgcount)
        return([dir_name[-1], r_avg, g_avg, b_avg])
    else:
        print(("No images in {0} directory successfully averaged")
            .format(dir_name[-1]))
        return(None)

def results_load_csv(csvin):
    """Accepts the path to a csv file formatted as follows:
    'File or Folder', 'Red', 'Green', 'Blue' parses the file
    line by line skipping the header. Returns a list containing
    an list for each line in the csv. Does not do any input checks
    other than converting the r, g, b colums to ints.
    """
    results = []
    with open(csvin, "rt") as f:
        read = csv.reader(f, delimiter=',')
        for row in read:
            if row[0] in ['File','Folder','File or Folder']:
                print('Skipping header')
            else:
                try:
                    row = [row[0], int(row[1]), int(row[2]), int(row[3])]
                    results.append(row)
                except Exception as e:
                    print(e)
    return(results)

def nested_directory_average(root_folder):
    """Accepts the path to a directory and walks all the enclosed
    directories calling average_directory for each one that
    contains images. Returns a list with the results of with an
    entry for each directory that was averaged.
    """
    dpaths = []
    filtered_dpaths= []
    results = []
    for dir_path, dir_names, files in os.walk(root_folder):
        dpaths.append(dir_path)
    for dpath in dpaths:
        for fname in os.listdir(dpath):
            filepath = os.path.join(dpath, fname)
            try:
                if imghdr.what(filepath) in ['jpeg','png']:
                    filtered_dpaths.append(dpath)
                    break
            except(IsADirectoryError):
                pass
    for dpath in filtered_dpaths:
        result = average_directory(dpath)
        try:
            if len(result) == 4:
                results.append(result)
        except:
            pass
    return(results)

def images_to_results(dirin):
    """Accepts the path to a directory averages each individual
    image and returns a list with and entry for each image
    successfully averaged.
    """
    try:
        cpus = cpu_count()
    except(NotImplementedError):
        cpus = 4
    images = []
    results = []
    files = [f for f in os.listdir(dirin)
        if os.path.isfile(os.path.join(dirin, f))]
    for f in files:
        filepath = os.path.join(dirin, f)
        if imghdr.what(filepath) in ['jpeg','png']:
            images.append(filepath)
    with Pool(cpus) as p:
        results = (p.map(avg_single_img, images))
    return(results)

def line_from_results(results):
    """Accepts a list of results and creates an image that is 1
    pixel tall and the length of the number of results. The
    image contains a pixel of the color of each result in the
    list of results. Returns a PIL Image object that can then
    be further manipulated or saved as desired.
    """
    if len(results) == 0:
        print("Nothing in results")
    else:
        im = Image.new("RGB", (len(results), 1),
            "hsl(0, 50%, 50%)")
        grid = im.load()
        for x in list(range(im.size[0])):
            grid[x,0] = (int(results[x][1]),
                      int(results[x][2]),
                      int(results[x][3]))
        return(im)

def rectangle_from_results(results, aspectratio=None):
    """Accepts a list of results and creates an image that is
    rectangular. The aspect ratio can be set by passing a list
    formated as [16,9] to aspectratio. The default is 3x2.
    The image contains a pixel of the color of each result in
    the list of results. Returns a PIL Image object that can
    then be further manipulated or saved as desired.
    """
    if len(results) == 0:
        print("Nothing in results")
    else:
        if aspectratio is None:
            aspectratio = [3,2]
        sidelength = int(math.floor(math.sqrt(len(results)
            / (aspectratio[0] * aspectratio[1]))))
        width = sidelength * aspectratio[0]
        height = sidelength * aspectratio[1]
        im = Image.new("RGB", (width, height), "hsl(0, 50%, 50%)")
        grid = im.load()
        c = 0
        for y in list(range(im.size[1])):
            for x in list(range(im.size[0])):
                grid[x, y] = (int(results[c][1]),
                          int(results[c][2]),
                          int(results[c][3]))
                c += 1
        return(im)

def results_save_csv(results, csv_out):
    """Accepts the path to a new csv file and a list containing
    results.Writes the current results to a csv file which can
    be re-loaded again by using csv_to_results. The csv created
    is formatted as follows:
    'File or Folder', 'Red', 'Green', 'Blue'
    """
    if len(results) == 0:
        print("Nothing in results")
    else:
        with open(csv_out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['File or Folder',
                        'Red', 'Green', 'Blue'])
            for r in results:
                writer.writerow(r)
            f.close()
