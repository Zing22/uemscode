# -*- coding=utf8 -*-

### simply call img2feature with picture path!
##  author: Zing
###

from os import walk
from shutil import move

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.externals import joblib
from PIL import Image

from train import readDataset
from rawimg import randomName
from process import toBin, cropLetters
from img2feature import toFeature

TEST_DATA = 'feature/test.txt'
SAVE_TO = 'model.pkl'
TEMP_DIR = 'tmp/'
RAW_TEST = 'raw_test/'
RAW_DONE = 'raw_done/'


# Core function, input path of code picture(or Image obj), return the code!
def img2code(path):
    try:
        img = Image.open(path)
    except Exception as e:
        path.load()
        img = path
    bimg = toBin(img) # convert to `1` mode
    success, letters = cropLetters(bimg) # crop into four letter images
    if not success:
        return 'ERROR'

    # get features array
    features = []
    for letter in letters:
        # letter is an Image
        features.append([int(x) for x in toFeature(letter).split(' ')])

    # predict
    pre = clf.predict(features)

    code = ''.join([chr(x + ord('A')) for x in pre])

    return code


def readAllFiles(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return f


def main():
    global clf
    clf = joblib.load(SAVE_TO)

    # do raw test
    err, total = 0,0
    for file in readAllFiles(RAW_TEST):
        name = img2code(Image.open(RAW_TEST + file))
        if name != 'ERROR':
            move(RAW_TEST+file, RAW_DONE+name+'.jpg')
        else:
            err += 1
        total += 1

    print('Done, check it and do error correction.')
    print('Error: {err}/{total}'.format(err = err, total = total))
    return


if __name__ == '__main__':
    main()